import discord
from discord.ext import commands
import openai
import os
import logging
import random
import requests
from discord.ui import Button, View



intents = discord.Intents.default()
intents.messages = False
clima_command = commands.Bot(command_prefix="a!", intents=intents)
OPENWEATHERMAP_API_KEY = 'e1770d669fd28c05cd483bde24ec27a2'

# Dicionário de tradução
weather_translations = {
    "broken clouds": "com nuvens quebradas",
    "clear sky": "com o céu limpo",
    "few clouds": "com poucas nuvens",
    "scattered clouds": "com nuvens dispersas",
    "overcast clouds": "nublado",
    # Adicione outras condições conforme necessário
}

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": OPENWEATHERMAP_API_KEY,
        "units": "metric",  # Unidades métricas para Celsius
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if response.status_code == 200:
        weather_description = data["weather"][0]["description"]
        weather_code = data["weather"][0]["id"]
        temperature = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        pressure = data["main"]["pressure"]
        wind_speed = data["wind"]["speed"]

        weather_image_url = get_weather_image_url(weather_code)

        # Chama a função para obter a URL da imagem
        weather_image_url = get_weather_image_url(weather_code)
        # Tradução manual usando o dicionário de tradução
        translated_description = weather_translations.get(weather_description.lower(), weather_description)

        embed = discord.Embed(
            title=f"Aurora, a jornalista climática tá na área! Vamos ver a temperatura em {city}?",
            description=f"Atualmente, está **{translated_description}**, eaí gosta desse clima?\n\n A temperatura no momento é de **{temperature}**°C. Acompanhe mais informações abaixo:\n",
            color=0xFFC0CB  # Cor azul, você pode ajustar conforme necessário
        )

        embed.set_thumbnail(url="https://i.imgur.com/EUllrKm.jpg")
        embed.add_field(name="\nA Sensação Térmica", value=f" é de **{feels_like}°C**", inline=True)
        embed.add_field(name="Umidade do Ar", value=f"**{humidity}%**", inline=True)
        embed.add_field(name="\nPressão Atmosférica", value=f"**{pressure} hPa**, afinal, alguém liga pra isso?", inline=False)
        embed.add_field(name="\nVelocidade do Vento", value=f"**{wind_speed} m/s**, será q da pra soltar uma pipa?", inline=True)
        embed.set_image(url=weather_image_url)

        return embed
    else:
        return "Não foi possível obter informações sobre o clima."
    
PEXELS_API_KEY = 't1J60ZLwJ13EenY7eNfcpJMIaSTpVdtbiAMMz8CXSysRXZHjwx1PKw8a'


async def search_pexels(query):
    url = 'https://api.pexels.com/v1/search'
    params = {
        'query': query,
        'per_page': 3,  # número de resultados desejados
    }
    headers = {
        'Authorization': PEXELS_API_KEY,
    }

    response = requests.get(url, params=params, headers=headers)

    if response.status_code == 200:
        data = response.json()
        return [photo['src']['original'] for photo in data.get('photos', [])]
    else:
        return None
    
def get_weather_image_url(weather_code):
    # Mapeie os códigos de condição meteorológica para URLs de imagens
    # Este é apenas um exemplo, você pode ajustar conforme necessário
    if 200 <= weather_code < 300:  # Trovões
        return "https://upload.wikimedia.org/wikipedia/commons/2/22/Lightning_14.07.2009_20-42-33.JPG"
    elif 300 <= weather_code < 600:  # Chuva
        return "https://imagens-cdn.canalrural.com.br/wp-content/uploads/chuvas-rapidas-frente-fria-previsao-do-tempo.jpg"
    elif 600 <= weather_code < 700:  # Neve
        return "https://img.freepik.com/fotos-gratis/3d-render-de-um-fundo-de-natal-com-neve-caindo_1048-15192.jpg"
    elif 800 == weather_code:  # Céu limpo
        return "https://t4.ftcdn.net/jpg/04/98/84/97/360_F_498849735_BuTCni2zojjI8HSWMkeSLTsnJZDOAPvE.jpg"
    elif 801 <= weather_code <= 804:  # Nublado
        return "https://img.freepik.com/fotos-gratis/chuva-preto-do-poder-escuro-abstrato_1127-2380.jpg"
    else:
        return "https://cdn.noticiasagricolas.com.br/dbimagens/thumbs/382x214-ar/previsao-de-tempo-5aZ36.jpg"
    
# Função para criar um embed da roleta girando
def create_roleta_embed():
    
    embed1 = discord.Embed(
        title="CASSINO DA AURORA",
        description="A roleta está girando...",
        color=0xFF5733  # Cor laranja, você pode alterar para a cor desejada
    )

    # Adicione a imagem da roleta diretamente ao embed
    embed1.set_image(url="https://4.bp.blogspot.com/-sFJ62-voC40/VnN5sJcAFbI/AAAAAAAARnk/FbKZH6eYz00/s400/roleta.gif")
    embed1.set_thumbnail(url="https://i.imgur.com/4rWXGIN.jpg")
    return embed1

# Função para criar um embed com o resultado da aposta
def create_resultado_embed(mensagem, imagem):
    
    embed2 = discord.Embed(title="E o resultado da aposta é: ", description=mensagem, color=0xFF0000)  # Cor vermelha, você pode alterar conforme desejado
    embed2.set_image(url=f"{imagem}")
    embed2.set_thumbnail(url="https://i.imgur.com/4rWXGIN.jpg")
    return embed2
    

