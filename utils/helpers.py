import qrcode
import asyncio
from io import BytesIO
from models import AdminActions
from utils import panel
from utils.log import logger
from marzban import UserModify, UserResponse


async def create_qr(text: str) -> bytes:
    """Create a QR code from the given text and return it as bytes."""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=7,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    # Create the QR image with custom colors
    qr_img = qr.make_image(fill_color="black", back_color="transparent").convert("RGBA")

    # Convert the image to bytes
    img_bytes_io = BytesIO()
    qr_img.save(img_bytes_io, "PNG")
    return img_bytes_io.getvalue()


async def process_user(
    semaphore: asyncio.Semaphore,
    user: UserResponse,
    tag: str,
    protocol: str,
    action: AdminActions,
    max_retries: int = 3
) -> bool:
    """Process a single user with semaphore for rate limiting and retry mechanism"""
    async with semaphore:
        for attempt in range(max_retries):
            try:
                current_inbounds = user.inbounds.copy() if user.inbounds else {}
                current_proxies = user.proxies.copy() if user.proxies else {}
                
                needs_update = False
                
                if action == AdminActions.Delete:
                    if protocol in current_inbounds and tag in current_inbounds[protocol]:
                        current_inbounds[protocol].remove(tag)
                        needs_update = True
                    
                    if not current_inbounds[protocol]:
                        current_inbounds.pop(protocol)
                        current_proxies.pop(protocol, None)
                
                elif action == AdminActions.Add:
                    if protocol not in current_inbounds:
                        current_inbounds[protocol] = []
                        current_proxies[protocol] = {}
                        needs_update = True
                
                if tag not in current_inbounds.get(protocol, []):
                    if protocol not in current_inbounds:
                        current_inbounds[protocol] = []
                    current_inbounds[protocol].append(tag)
                    needs_update = True
                
                if not needs_update:
                    return True
                
                update_data = UserModify(
                    proxies=current_proxies,
                    inbounds=current_inbounds,
                )
                
                success = await panel.user_modify(user.username, update_data)
                
                if success:
                    return True
                
            except Exception as e:
                logger.error(f"Error processing user {user.username} (Attempt {attempt + 1}): {e}")
                
                await asyncio.sleep(0.5 ** attempt)
        
        logger.error(f"Failed to process user {user.username} after {max_retries} attempts")
        return False


async def process_batch(
    users: list[UserResponse], tag: str, protocol: str, action: AdminActions
) -> int:
    """Process a batch of users concurrently with rate limiting"""
    semaphore = asyncio.Semaphore(5)
    tasks = []

    for user in users:
        task = asyncio.create_task(process_user(semaphore, user, tag, protocol, action))
        tasks.append(task)

    results = await asyncio.gather(*tasks)
    return sum(results)


async def manage_panel_inbounds(tag: str, protocol: str, action: AdminActions) -> bool:
    try:
        offset = 0
        batch_size = 25
        total_updated = 0

        while True:
            users = await panel.get_users(offset)
            if not users:
                break

            batch_updated = await process_batch(users, tag, protocol, action)
            total_updated += batch_updated
            
            if len(users) < batch_size:
                break
            offset += batch_size

            await asyncio.sleep(1.0)

        return True

    except Exception as e:
        logger.error(f"Error in manage panel inbounds: {e}")
        return False