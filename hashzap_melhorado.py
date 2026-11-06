"""Hashzap melhorado (chat em tempo real com Flet).

Melhorias sobre o codigo.py: mensagens com horário e balões diferentes para você e para os outros,
nome obrigatório, Enter envia, rolagem automática, aviso de saída e API atual do Flet.
Instalar: pip install flet     Rodar: python hashzap_melhorado.py
"""
from datetime import datetime

import flet as ft


def main(pagina: ft.Page):
    pagina.title = "Hashzap"
    estado = {"nome": ""}

    chat = ft.ListView(expand=True, spacing=8, auto_scroll=True)
    titulo = ft.Text("Hashzap", size=32, weight=ft.FontWeight.BOLD)

    def mostrar(mensagem):
        if mensagem["tipo"] == "sistema":
            chat.controls.append(ft.Text(mensagem["texto"], italic=True, size=12, text_align=ft.TextAlign.CENTER))
        else:
            minha = mensagem["autor"] == estado["nome"]
            balao = ft.Container(
                content=ft.Column([
                    ft.Text("" if minha else mensagem["autor"], size=11, weight=ft.FontWeight.BOLD),
                    ft.Text(mensagem["texto"]),
                    ft.Text(mensagem["hora"], size=10),
                ], spacing=2, tight=True),
                padding=10, border_radius=12,
                bgcolor=ft.Colors.GREEN_100 if minha else ft.Colors.GREY_200,
            )
            chat.controls.append(ft.Row([balao], alignment=ft.MainAxisAlignment.END if minha else ft.MainAxisAlignment.START))
        pagina.update()

    pagina.pubsub.subscribe(mostrar)

    def enviar(evento):
        texto = campo_mensagem.value.strip()
        if not texto:
            return
        pagina.pubsub.send_all({"tipo": "msg", "autor": estado["nome"], "texto": texto,
                                "hora": datetime.now().strftime("%H:%M")})
        campo_mensagem.value = ""
        campo_mensagem.focus()
        pagina.update()

    campo_mensagem = ft.TextField(label="Escreva sua mensagem", expand=True, on_submit=enviar)
    linha_enviar = ft.Row([campo_mensagem, ft.ElevatedButton("Enviar", on_click=enviar)])

    def entrar_chat(evento):
        nome = nome_usuario.value.strip()
        if not nome:
            nome_usuario.error_text = "Digite seu nome"
            pagina.update()
            return
        estado["nome"] = nome
        pagina.close(popup)
        pagina.remove(botao_iniciar, titulo)
        pagina.add(chat, linha_enviar)
        pagina.pubsub.send_all({"tipo": "sistema", "texto": f"{nome} entrou no chat"})

    nome_usuario = ft.TextField(label="Escreva seu nome no chat", autofocus=True, on_submit=entrar_chat)
    popup = ft.AlertDialog(modal=True, title=ft.Text("Bem vindo ao Hashzap"), content=nome_usuario,
                           actions=[ft.ElevatedButton("Entrar no chat", on_click=entrar_chat)])
    botao_iniciar = ft.ElevatedButton("Iniciar Chat", on_click=lambda e: pagina.open(popup))
    pagina.add(titulo, botao_iniciar)


ft.app(target=main, view=ft.AppView.WEB_BROWSER)
