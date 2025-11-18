#!/usr/bin/env python3
"""
Script para renovar o token de autenticação do YouTube
Execute este script quando o token expirar
"""
import os
import sys
from youtube_uploader import YouTubeUploader

def main():
    print("=" * 60)
    print("🔄 RENOVANDO TOKEN DE AUTENTICAÇÃO DO YOUTUBE")
    print("=" * 60)
    
    # Remove token antigo se existir
    token_file = 'credentials/token.pickle'
    if os.path.exists(token_file):
        print(f"🗑️  Removendo token antigo: {token_file}")
        os.remove(token_file)
        print("✅ Token antigo removido")
    
    # Verifica se credentials.json existe
    credentials_file = 'credentials/credentials.json'
    if not os.path.exists(credentials_file):
        print(f"❌ Arquivo de credenciais não encontrado: {credentials_file}")
        print("📝 Você precisa criar este arquivo com suas credenciais do Google Cloud Console")
        print("🔗 https://console.cloud.google.com/apis/credentials")
        return False
    
    print("\n🔐 Iniciando autenticação...")
    print("💡 Uma janela do navegador será aberta para você fazer login")
    print("💡 Após fazer login, o token será salvo automaticamente\n")
    
    try:
        # Cria novo uploader (isso vai solicitar nova autenticação)
        uploader = YouTubeUploader()
        
        if uploader.youtube:
            print("\n✅ Token renovado com sucesso!")
            print("✅ Você pode usar o bot normalmente agora")
            return True
        else:
            print("\n❌ Falha ao renovar token")
            return False
            
    except Exception as e:
        print(f"\n❌ Erro ao renovar token: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

