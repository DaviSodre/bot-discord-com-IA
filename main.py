import discord
from discord.ext import commands
from discord import app_commands
import openai
from dotenv import load_dotenv
import os
from comandos import *
from database_config import *
from database_config import get_all_users_sorted_by_level_xp






load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GPT_TOKEN = os.getenv("GPT_TOKEN")

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix="a!", intents=intents)


client, db, xp_collection = connect_to_database()

openai.api_key = GPT_TOKEN

mensagens = [{"role": "system", "content": "A partir de agora atue como uma pessoa que responde dúvidas e conversa com as pessoas! Use linguagem adolescente e gentil. Seu nome é Meowtopia e você é do genero feminino!"},]




async def ask_gpt(mensagens, message):

    mensagens = [mensagens[0]] + mensagens[-9:]

    
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=mensagens,
            max_tokens=250,
            temperature=1
         )
    return response['choices'][0]['message']['content']
        
    

@bot.event
async def on_ready():
    print(f"Oi, eu sou {bot.user.name} e estou acordada!")

    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="Entre no nosso servidor!\n\n https://discord.gg/meowtopia"))
    try:
        synced = await bot.tree.sync()
        print(f"Sincronizado {len(synced)} comandos")
    except Exception as e:
        print(e)


COOLDOWN = 10

# Crie um dicionário para rastrear o último uso do comando por cada usuário
cooldowns = {}


@bot.tree.command(name="coins")
async def check_coins(interaction: discord.Interaction):
    # Obtenha o ID do usuário da interação
    user_id = interaction.user.id

    # Obtenha os dados do usuário com base no ID
    user_data = get_user_data(user_id)
    
    await interaction.response.send_message(f"<:redcherry:1206507976324681738> | Você tem **{user_data['coins']}** Coins.")

@bot.tree.command(name="rank")
async def show_rank(interaction: discord.Interaction):
    # Obtenha o ID do usuário da interação
    user_id = interaction.user.id

    # Obtenha os dados do usuário com base no ID
    user_data = get_user_data(user_id)

    # Calcula o XP necessário para o próximo nível
    xp_needed = calculate_xp_needed(user_data["level"])

    # Calcula o XP total do próximo nível
    total_xp_next_level = user_data["xp"] + xp_needed

    # Crie um embed para a mensagem de rank
    embed = discord.Embed(
        title=f"Rank de {interaction.user.name}",
        color=0x3498db  # Cor azul, você pode alterar para a cor desejada
    )

    # Adicione os campos ao embed
    embed.add_field(name="Nível", value=user_data['level'], inline=True)
    embed.add_field(name="XP Atual", value=user_data['xp'], inline=False)
    embed.add_field(name="XP Necessário para o Próximo Nível", value=xp_needed, inline=False)
    embed.add_field(name="Total de XP para o Próximo Nível", value=total_xp_next_level, inline=True)

    # Defina a miniatura como o avatar do usuário
    embed.set_thumbnail(url=interaction.user.avatar.url)

    # Envie o embed como resposta à interação
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="top")
async def top_rank(interaction: discord.Interaction):
    # Obtém a lista de usuários ordenados por nível e XP
    users = get_all_users_sorted_by_level_xp()
    
    # Crie um embed para a mensagem de rank
    embed = discord.Embed(
        title="<a:b_hrt2:1206490678436302910> | Ranking Global",
        color=0x3498db
    )

    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/427/427687.png")

    # Verifique se há usuários na lista
    if not users:
        embed.description = "Não há usuários para exibir no ranking."
    else:
        # Adicione os campos ao embed
        for index, user in enumerate(users[:10], start=1):
            # Obtém o nome de exibição no momento da exibição
            user_data = get_user_data(user['user_id'])
            user_name = user_data.get('user_name', 'Usuário Desconhecido')
            
            level = user.get("level", "N/A")
            xp = user.get("xp", "N/A")

            xp_needed = calculate_xp_needed(user_data["level"])
            embed.add_field(name=f"{index}. {user_name}", value=f"Nível: {user['level']} | XP: {user['xp']}/{xp_needed}", inline=False)

        # Define uma miniatura personalizada (ícone de troféu)
       
    # Envie o embed como resposta à interação
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="baltop")
async def top_rank_coins(interaction: discord.Interaction):
      # Obtém a lista de usuários ordenados por nível e XP
      users = get_all_users_sorted_by_coins()

      # Crie um embed para a mensagem de rank
      embed = discord.Embed(
          title="Ranking Global",
          color=0x3498db
      )

      embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/427/427687.png")

      # Verifique se há usuários na lista
      if not users:
          embed.description = "Não há usuários para exibir no ranking."
      else:
          # Adicione os campos ao embed
          for index, user in enumerate(users[:10], start=1):
              # Obtém o nome de exibição no momento da exibição
              user_data = get_user_data(user['user_id'])
              user_name = user_data.get('user_name', 'Usuário Desconhecido')

              coins = user.get("level", "N/A")

              embed.add_field(name=f"{index}. {user_name}", value=f"Coins: {user['coins']}", inline=False)

          # Define uma miniatura personalizada (ícone de troféu)

        
              
              

      # Envie o embed como resposta à interação
      await interaction.response.send_message(embed=embed)

    

@bot.tree.command(name="perfil")
async def show_profile(interaction: discord.Interaction, user: discord.User = None):
    # Obtenha o ID do usuário da interação ou do usuário mencionado (se fornecido)
    target_user_id = str(user.id) if user else str(interaction.user.id)
    target_user_id2 = (user.id) if user else (interaction.user.id)
    
    
    # Obtenha os dados do usuário
    user_data = get_user_data(target_user_id)
    user_data2 = get_user_data(target_user_id2)
    xp_needed = calculate_xp_needed(user_data2["level"])

    # Crie um embed para o perfil do usuário
    embed = discord.Embed(
        title=f"Perfil de {user.name if user else interaction.user.name}",
        color=0xFFC0CB
    )

    # Converta os valores de XP e nível para strings
    level_str = str(user_data2['level'])
    xp_str = str(user_data2['xp'])
    coins_str = str(user_data2['coins'])

    # Adicione os campos ao embed
    embed.add_field(name="Nível", value=level_str, inline=True)
    embed.add_field(name="XP", value=f'{xp_str}/{xp_needed}', inline=True)
    embed.add_field(name="Coins", value=coins_str, inline=True)
    embed.add_field(name="Sobre mim: ", value=user_data['about_me'], inline=False)
    embed.set_image(url=user_data['background_image'])
    embed.set_footer(text="Meowtopia - Link do servidor na bio!", icon_url=bot.user.avatar.url)
    

    # Defina a miniatura como o avatar do usuário
    if user:
        embed.set_thumbnail(url=user.avatar.url)
    else:
        embed.set_thumbnail(url=interaction.user.avatar.url)

    # Envie o embed como resposta à interação
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="sobremim")
async def set_about_me(interaction: discord.Interaction, sobre_mim: str):
    user_id = str(interaction.user.id)  # Utilize interaction.user.id ao invés de interaction.author.id
    user_data = get_user_data(user_id)
    
    # Define a nova mensagem "Sobre Mim"
    user_data["about_me"] = sobre_mim

    # Atualiza os dados do usuário
    set_user_data(user_data, interaction.user.display_name)

    await interaction.response.send_message("'Sobre mim' atualizado com sucesso! Verifique usando /perfil!")

@bot.tree.command(name="setbackground")
async def set_background_image(interaction: discord.Interaction, background_url: str):
    user_id = str(interaction.user.id)
    user_data = get_user_data(user_id)

    # Atualize o campo 'background_image' com a nova URL
    user_data['background_image'] = background_url

    # Salve os dados atualizados no banco de dados
    set_user_data(user_data, interaction.user.display_name)

    await interaction.response.send_message(content=f"Fundo de perfil atualizado para: {background_url}")

@bot.tree.command(name="clima")
async def clima(interaction: discord.Interaction, cidade: str):
    resultado = get_weather(cidade)
    if isinstance(resultado, discord.Embed):
        await interaction.response.send_message(embed=resultado)
    else:
        await interaction.response.send_message(f"Desculpe, não foi possível encontrar informações para a cidade '**{cidade}**'. Verifique se o nome da cidade está correto.")
    
def calculate_xp_needed(current_level):
    return int(100 * 1.5**current_level)
def calculate_coins_needed(current_level):
    # Modifique a fórmula conforme necessário
    return int(100 * 1.5**current_level)


@bot.event
async def on_message(message):
    bot_especifico_id = "981295581269983232"
    user = message.author

    if message.author.bot and message.author.id != int(bot_especifico_id):
        return
   
    
    user_data = get_user_data(message.author.id)
    
    # Lógica para ganhar XP
    xp_earned = 5  # Ajuste conforme necessário
    user_data["xp"] += xp_earned

     # Lógica para ganhar moedas
    coins_earned = 10  # Ajuste conforme necessário
    user_data["coins"] += coins_earned
    SERVIDOR_PROIBIDO_ID = '1142651005926920304'


    while user_data["xp"] >= calculate_xp_needed(user_data["level"]):
        user_data["xp"] -= calculate_xp_needed(user_data["level"])
        user_data["level"] += 1
        if message.guild.id != SERVIDOR_PROIBIDO_ID:
         user_data["coins"] += calculate_coins_needed(user_data["level"])
         await message.reply(f"Parabéns! Você subiu para o nível {user_data['level']} e ganhou {calculate_coins_needed(user_data['level'])} coins!")

    # Atualiza os dados do usuário no banco de dados
    set_user_data(user_data, message.author.display_name)

    # Processa comandos Discord.py
    await bot.process_commands(message)

    # Verifica se o bot é mencionado
    if bot.user.mentioned_in(message):
        async with message.channel.typing():
            # Obtém o apelido (nick) do autor da mensagem, se existir
            user_nick = message.author.nick if message.author.nick else message.author.name
            # Adiciona mensagens anteriores à lista de conversa
            mensagens.append({"role": "user", "content": f"Mensagem de {user_nick}: {message.content}"})

            # Gera resposta do modelo
            resposta = await ask_gpt(mensagens, message)

              # Adiciona a resposta à lista de mensagens
            mensagens.append({"role": "system", "content": resposta})
            
            await message.reply(resposta)
            print(message.content)
            print(resposta)
           


bot.run(DISCORD_TOKEN)
