import asyncio
import os
from eclipse import get_value

class Manager:
    def __init__(self, client):
        self.client = client
        self.sudo_users = get_value("sudo_users")

    async def edit_or_reply(
        self,
        event,
        text,
        parse_mode=None,
        link_preview=None,
    ):
        link_preview = link_preview or False
        parse_mode = parse_mode or "md"
        reply_to = await event.get_reply_message()
        
        if len(text) < 4096 and not def_link:
            parse_mode = parse_mode or "md"
            if event.sender_id in self.sudo_users:
                if reply_to:
                    return await reply_to.reply(
                        text, parse_mode=parse_mode, link_preview=link_preview
                    )
                return await event.reply(
                    text, parse_mode=parse_mode, link_preview=link_preview
                )
            await event.edit(text, parse_mode=parse_mode, link_preview=link_preview)
            return event

    async def edit_delete(
        self,
        event,
        text,
        time=None,
        parse_mode=None,
        link_preview=None
    ):
        parse_mode = parse_mode or "md"
        link_preview = link_preview or False
        time = time or 10

        if event.sender_id in self.sudo_users:
            reply_to = await event.get_reply_message()
            return (
                await reply_to.reply(text, link_preview=link_preview, parse_mode=parse_mode)
                if reply_to
                else await event.reply(text, link_preview=link_preview, parse_mode=parse_mode)
            )
        else:
            return await event.edit(
                text, link_preview=link_preview, parse_mode=parse_mode
            )

        await asyncio.sleep(time)
        return await event.delete()

