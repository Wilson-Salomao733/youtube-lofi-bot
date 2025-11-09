#!/usr/bin/env python3
"""
Script para fazer login no YouTube uma vez e salvar cookies
Execute este script uma vez para salvar seu login
"""
import os
import sys
import time
from youtube_automation import YouTubeAutomation
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)

logger = logging.getLogger(__name__)


def main():
    """Faz login e salva cookies"""
    print("=" * 70)
    print("🔐 SALVAR LOGIN DO YOUTUBE")
    print("=" * 70)
    print("\nEste script:")
    print("  1️⃣  Abre o navegador")
    print("  2️⃣  Você faz login no YouTube")
    print("  3️⃣  Salva os cookies para uso futuro")
    print("\n💡 Você só precisa fazer isso UMA VEZ")
    print("=" * 70)
    
    automation = YouTubeAutomation(headless=False)
    
    try:
        print("\n🌐 Abrindo navegador...")
        if not automation._setup_driver():
            print("❌ Erro ao abrir navegador")
            return False
        
        print("\n📝 INSTRUÇÕES:")
        print("  1. O navegador abrirá automaticamente")
        print("  2. Faça login no YouTube/Google")
        print("  3. Aguarde até ver a página do YouTube Studio")
        print("  4. Os cookies serão salvos automaticamente")
        print("\n⏳ Aguardando você fazer login...")
        print("   (Pressione Ctrl+C para cancelar)\n")
        
        # Faz login (aguarda até fazer login)
        if automation.login_youtube():
            print("\n" + "=" * 70)
            print("✅ LOGIN SALVO COM SUCESSO!")
            print("=" * 70)
            print(f"📁 Cookies salvos em: {automation.cookies_file}")
            print("💡 Agora você pode usar os scripts sem precisar fazer login novamente!")
            print("=" * 70)
            
            # Mantém navegador aberto por alguns segundos
            print("\n⏳ Fechando navegador em 5 segundos...")
            time.sleep(5)
            
            return True
        else:
            print("\n❌ Não foi possível salvar login")
            print("💡 Tente executar o script novamente")
            return False
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Operação cancelada pelo usuário")
        return False
    except Exception as e:
        logger.error(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        automation.close()


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

