import asyncio
import discord
from discord.ext import commands
import noticesystem 


class MyCommands(commands.Cog):

  def __init__(self, bot: commands.Bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_ready(self):
    print("Cog с командами успешно загружен!")

  @commands.command(name="removenotice", help="Удалить заметку")
  async def removenotice(
      self, ctx: commands.Context, user: discord.Member = None
  ):
    target_user = user or ctx.author
    username = target_user.name

    await ctx.send(
        f"🚫 Хочешь удалить заметку пользователя **{username}**?\n"
        f"Напиши в чат точное **название** заметки, которую нужно стереть:"
    )

    def check(message: discord.Message):
      return message.author == ctx.author and message.channel == ctx.channel

    try:
      msg = await self.bot.wait_for("message", check=check, timeout=60.0)
      title_to_delete = msg.content.strip()

      success = noticesystem.deletenotice(target_user.id, title_to_delete)

      if success:
        await ctx.send(
            f"🗑️ Заметка **'{title_to_delete}'** пользователя **{username}** успешно удалена!"
        )
      else:
        await ctx.send(
            f"❌ Заметка с названием **'{title_to_delete}'** не найдена у пользователя **{username}**."
        )

    except asyncio.TimeoutError:
      await ctx.send(f"⏱️ {ctx.author.mention}, время ожидания ответа истекло.")





  @commands.command(name="notice", help="создать/посмотреть текущую заметку")
  async def notice(self, ctx: commands.Context, user: discord.Member = None):
    print("Notice Command!")

    target_user = user or ctx.author
    username = target_user.name

    await ctx.send(
        f"🪵 Привет, {username}!\n"
        f"Напиши в чат **Создать** или **Проверить**, чтобы выбрать действие."
    )

    def check(message: discord.Message):
      return message.author == ctx.author and message.channel == ctx.channel

    try:
      msg = await self.bot.wait_for("message", check=check, timeout=30.0)
      content = msg.content.lower().strip()

      if content == "создать":
        await ctx.send("📝 Введите **название** для вашей заметки:")
        title_msg = await self.bot.wait_for(
            "message", check=check, timeout=60.0
        )
        title = title_msg.content.strip()

        await ctx.send("⏰ Теперь введите **дату и время** (например, 25.10 18:00):")
        date_msg = await self.bot.wait_for("message", check=check, timeout=60.0)
        date_text = date_msg.content.strip()

        noticesystem.createnotice(target_user.id, title, date_text)
        await ctx.send(
            f"✅ Заметка **'{title}'** успешно сохранена на **{date_text}**!"
        )

      elif content == "проверить":
        notices = noticesystem.getnotices(target_user.id)

        if not notices:
          await ctx.send(f"📂 У пользователя **{username}** пока нет заметок.")
        else:
          response_text = f"📋 **Текущие заметки для {username}**:\n\n"
          for index, (title, notice_date) in enumerate(notices, start=1):
            response_text += f"{index}. **{title}** — ⏰ *{notice_date}*\n"

          await ctx.send(response_text)

      else:
        await ctx.send(
            f"Неизвестная команда '{msg.content}'. Пожалуйста, повторите вызов команды."
        )

    except asyncio.TimeoutError:
      await ctx.send(f"⏱️ {ctx.author.mention}, время ожидания ответа истекло.")


async def setup(bot: commands.Bot):
  await bot.add_cog(MyCommands(bot))
