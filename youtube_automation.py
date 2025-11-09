"""
Módulo de automação web para YouTube Studio
Automatiza o clique no botão "Transmitir ao vivo" quando ffmpeg não está disponível
"""
import os
import time
import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException

logger = logging.getLogger(__name__)

# Arquivo para salvar cookies
COOKIES_FILE = "credentials/youtube_cookies.json"


class YouTubeAutomation:
    """Automação web para YouTube Studio"""
    
    def __init__(self, headless=False):
        """
        Inicializa a automação
        
        Args:
            headless: Se True, executa o navegador em modo headless (sem interface)
        """
        self.driver = None
        self.headless = headless
        self.wait_timeout = 30
        self.cookies_file = COOKIES_FILE
        # Garante que o diretório existe
        os.makedirs(os.path.dirname(self.cookies_file), exist_ok=True)
    
    def _setup_driver(self):
        """Configura o driver do Selenium"""
        try:
            chrome_options = Options()
            
            # Configurações para Docker/headless
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_argument('--user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            
            # Verifica se está no Docker ou precisa de headless
            is_docker = os.path.exists('/.dockerenv') or os.environ.get('DOCKER_CONTAINER') == 'true'
            
            if self.headless or is_docker:
                chrome_options.add_argument('--headless')
                chrome_options.add_argument('--disable-extensions')
                logger.info("🖥️  Modo headless ativado (Docker ou configurado)")
            
            # Tenta usar Chromium (comum no Docker) ou Chrome
            chromium_bin = os.environ.get('CHROME_BIN', '/usr/bin/chromium')
            if os.path.exists(chromium_bin):
                chrome_options.binary_location = chromium_bin
                logger.info(f"🔍 Usando Chromium: {chromium_bin}")
            
            # Tenta usar Chrome/Chromium
            try:
                self.driver = webdriver.Chrome(options=chrome_options)
                logger.info("✅ Chrome/Chromium driver inicializado")
                return True
            except Exception as e:
                logger.warning(f"⚠️  Chrome/Chromium não encontrado: {e}")
                logger.info("💡 Tentando Firefox...")
                
                # Tenta usar Firefox
                try:
                    from selenium.webdriver.firefox.options import Options as FirefoxOptions
                    firefox_options = FirefoxOptions()
                    if self.headless or is_docker:
                        firefox_options.add_argument('--headless')
                    self.driver = webdriver.Firefox(options=firefox_options)
                    logger.info("✅ Firefox driver inicializado")
                    return True
                except Exception as e2:
                    logger.error(f"❌ Firefox também não encontrado: {e2}")
                    logger.error("💡 Instale Chrome, Chromium ou Firefox no sistema")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Erro ao configurar driver: {e}")
            return False
    
    def save_cookies(self):
        """Salva os cookies do navegador para reutilizar depois"""
        if not self.driver:
            return False
        
        try:
            # Salva cookies de múltiplos domínios
            cookies_to_save = []
            
            # Cookies do YouTube
            try:
                self.driver.get("https://www.youtube.com/")
                time.sleep(1)
                cookies_to_save.extend(self.driver.get_cookies())
            except:
                pass
            
            # Cookies do Google
            try:
                self.driver.get("https://accounts.google.com/")
                time.sleep(1)
                cookies_to_save.extend(self.driver.get_cookies())
            except:
                pass
            
            # Remove duplicatas
            seen = set()
            unique_cookies = []
            for cookie in cookies_to_save:
                key = (cookie.get('name'), cookie.get('domain'))
                if key not in seen:
                    seen.add(key)
                    unique_cookies.append(cookie)
            
            with open(self.cookies_file, 'w') as f:
                json.dump(unique_cookies, f, indent=2)
            
            logger.info(f"✅ {len(unique_cookies)} cookies salvos em {self.cookies_file}")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Erro ao salvar cookies: {e}")
            return False
    
    def load_cookies(self):
        """Carrega cookies salvos no navegador"""
        if not self.driver:
            return False
        
        if not os.path.exists(self.cookies_file):
            logger.info("💡 Nenhum cookie salvo encontrado")
            return False
        
        try:
            # Primeiro acessa o domínio para poder adicionar cookies
            self.driver.get("https://www.youtube.com/")
            time.sleep(2)
            
            with open(self.cookies_file, 'r') as f:
                cookies = json.load(f)
            
            # Adiciona cada cookie
            added_count = 0
            for cookie in cookies:
                try:
                    # Remove campos que podem causar problemas
                    cookie_copy = cookie.copy()
                    cookie_copy.pop('sameSite', None)
                    # Mantém expiry mas converte se necessário
                    if 'expiry' in cookie_copy:
                        expiry = cookie_copy['expiry']
                        if isinstance(expiry, float):
                            cookie_copy['expiry'] = int(expiry)
                    
                    # Adiciona cookie
                    self.driver.add_cookie(cookie_copy)
                    added_count += 1
                except Exception as e:
                    logger.debug(f"⚠️  Erro ao adicionar cookie: {e}")
                    continue
            
            logger.info(f"✅ {added_count} cookies carregados de {self.cookies_file}")
            return added_count > 0
        except Exception as e:
            logger.warning(f"⚠️  Erro ao carregar cookies: {e}")
            return False
    
    def login_youtube(self):
        """
        Verifica se está logado no YouTube
        Tenta carregar cookies salvos primeiro
        """
        if not self.driver:
            if not self._setup_driver():
                return False
        
        try:
            # Tenta carregar cookies salvos
            if self.load_cookies():
                logger.info("🔄 Recarregando página com cookies...")
                self.driver.get("https://studio.youtube.com/")
                time.sleep(5)
            
            # Verifica se precisa fazer login
            current_url = self.driver.current_url.lower()
            
            if "accounts.google.com" in current_url or "signin" in current_url or "login" in current_url:
                logger.warning("⚠️  Login necessário detectado")
                logger.info("💡 Por favor, faça login manualmente no navegador que abriu")
                logger.info("💡 O script aguardará até você fazer login (pressione Ctrl+C para cancelar)")
                
                # Aguarda indefinidamente até fazer login (verifica a cada 5 segundos)
                max_wait_time = 300  # 5 minutos máximo
                waited = 0
                
                while waited < max_wait_time:
                    time.sleep(5)
                    waited += 5
                    
                    # Verifica se ainda está na página de login
                    try:
                        current_url = self.driver.current_url.lower()
                        if "accounts.google.com" not in current_url and "signin" not in current_url and "login" not in current_url:
                            # Pode ter feito login, verifica se está no YouTube Studio
                            if "studio.youtube.com" in current_url or "youtube.com" in current_url:
                                logger.info("✅ Login detectado! Continuando...")
                                time.sleep(3)  # Aguarda página carregar completamente
                                # Salva cookies para próxima vez
                                self.save_cookies()
                                break
                    except:
                        pass
                    
                    if waited % 30 == 0:  # A cada 30 segundos
                        remaining = max_wait_time - waited
                        logger.info(f"⏳ Aguardando login... ({remaining}s restantes)")
                
                # Verifica novamente após o loop
                try:
                    self.driver.refresh()
                    time.sleep(3)
                    current_url = self.driver.current_url.lower()
                    
                    if "accounts.google.com" in current_url or "signin" in current_url:
                        logger.error("❌ Ainda não está logado após 5 minutos.")
                        logger.error("💡 Por favor, faça login manualmente e execute o script novamente.")
                        return False
                except:
                    pass
            
            logger.info("✅ Acesso ao YouTube Studio confirmado")
            # Salva cookies se ainda não salvou
            if not os.path.exists(self.cookies_file):
                self.save_cookies()
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao acessar YouTube Studio: {e}")
            return False
    
    def go_to_live_stream(self, broadcast_id):
        """
        Navega para a página da live específica
        
        Args:
            broadcast_id: ID do broadcast da live
        """
        if not self.driver:
            return False
        
        try:
            url = f"https://studio.youtube.com/video/{broadcast_id}/livestreaming"
            logger.info(f"🌐 Navegando para: {url}")
            self.driver.get(url)
            time.sleep(5)  # Aguarda página carregar
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao navegar para live: {e}")
            return False
    
    def click_streaming_help_and_complete(self):
        """
        Clica em "Ajuda das configurações de streaming" e depois em "Concluído"
        Isso é necessário antes de poder clicar em "Transmitir ao vivo"
        """
        if not self.driver:
            return False
        
        try:
            logger.info("🔍 Procurando 'Ajuda das configurações de streaming'...")
            
            # Procura o link/botão de ajuda
            help_selectors = [
                "//a[contains(text(), 'Ajuda das configurações de streaming')]",
                "//button[contains(text(), 'Ajuda das configurações de streaming')]",
                "//a[contains(text(), 'streaming settings')]",
                "//button[contains(text(), 'streaming settings')]",
                "//a[contains(@href, 'streaming')]",
            ]
            
            help_link = None
            for selector in help_selectors:
                try:
                    wait = WebDriverWait(self.driver, 5)
                    help_link = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    logger.info("✅ Link de ajuda encontrado")
                    break
                except TimeoutException:
                    continue
            
            if help_link:
                logger.info("🖱️  Clicando em 'Ajuda das configurações de streaming'...")
                help_link.click()
                time.sleep(3)  # Aguarda modal abrir
                
                # Procura botão "Concluído"
                logger.info("🔍 Procurando botão 'Concluído'...")
                complete_selectors = [
                    "//button[contains(text(), 'Concluído')]",
                    "//button[contains(text(), 'Concluído') and contains(@class, 'yt-spec-button')]",
                    "//button[contains(text(), 'Done')]",
                    "//button[contains(@aria-label, 'Concluído')]",
                ]
                
                complete_button = None
                for selector in complete_selectors:
                    try:
                        wait = WebDriverWait(self.driver, 5)
                        complete_button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        logger.info("✅ Botão 'Concluído' encontrado")
                        break
                    except TimeoutException:
                        continue
                
                if complete_button:
                    logger.info("🖱️  Clicando em 'Concluído'...")
                    complete_button.click()
                    time.sleep(2)
                    logger.info("✅ Modal fechado")
                    return True
                else:
                    logger.warning("⚠️  Botão 'Concluído' não encontrado (pode já estar fechado)")
                    return True
            else:
                logger.info("💡 Link de ajuda não encontrado (pode não ser necessário)")
                return True
                
        except Exception as e:
            logger.warning(f"⚠️  Erro ao clicar em ajuda: {e}")
            return True  # Continua mesmo se falhar
    
    def click_go_live_button(self, max_retries=3):
        """
        Clica no botão "Transmitir ao vivo" no YouTube Studio
        Primeiro tenta clicar em "Ajuda das configurações" e "Concluído" se necessário
        
        Args:
            max_retries: Número máximo de tentativas
        
        Returns:
            True se sucesso, False caso contrário
        """
        if not self.driver:
            logger.error("❌ Driver não inicializado")
            return False
        
        # Primeiro, tenta clicar em "Ajuda" e "Concluído" se necessário
        self.click_streaming_help_and_complete()
        time.sleep(2)
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"🔍 Tentativa {attempt}/{max_retries}: Procurando botão 'Transmitir ao vivo'...")
                
                # Aguarda página carregar
                time.sleep(3)
                
                # Procura o botão "Transmitir ao vivo" por vários seletores possíveis
                button_selectors = [
                    # Seletor em português
                    "//button[contains(text(), 'Transmitir ao vivo')]",
                    "//button[contains(text(), 'Go live')]",
                    "//button[contains(@aria-label, 'Transmitir ao vivo')]",
                    "//button[contains(@aria-label, 'Go live')]",
                    # Por classe/ID comum
                    "//button[contains(@class, 'go-live')]",
                    "//button[@id='go-live-button']",
                    # Seletor genérico para botão de ação principal
                    "//button[contains(@class, 'yt-spec-button-shape-next') and contains(., 'vivo')]",
                    "//button[contains(@class, 'yt-spec-button-shape-next') and contains(., 'live')]",
                ]
                
                button = None
                for selector in button_selectors:
                    try:
                        wait = WebDriverWait(self.driver, 10)
                        button = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                        logger.info(f"✅ Botão encontrado com seletor: {selector}")
                        break
                    except TimeoutException:
                        continue
                
                if not button:
                    # Tenta encontrar por texto visível
                    logger.info("🔍 Tentando encontrar botão por texto visível...")
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for btn in buttons:
                        text = btn.text.lower()
                        if "transmitir" in text or "go live" in text or "vivo" in text:
                            button = btn
                            logger.info(f"✅ Botão encontrado por texto: {btn.text}")
                            break
                
                if not button:
                    logger.warning(f"⚠️  Botão não encontrado na tentativa {attempt}")
                    if attempt < max_retries:
                        logger.info("⏳ Aguardando 5 segundos antes de tentar novamente...")
                        time.sleep(5)
                        # Recarrega a página
                        logger.info("🔄 Recarregando página...")
                        self.driver.refresh()
                        time.sleep(5)
                        # Tenta ajuda novamente
                        self.click_streaming_help_and_complete()
                        time.sleep(2)
                    continue
                
                # Rola até o botão se necessário
                self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
                time.sleep(1)
                
                # Verifica se o botão está habilitado
                if not button.is_enabled():
                    logger.warning("⚠️  Botão encontrado mas está desabilitado")
                    if attempt < max_retries:
                        logger.info("⏳ Aguardando 5 segundos...")
                        time.sleep(60)
                        continue
                
                # Clica no botão
                logger.info("🖱️  Clicando no botão 'Transmitir ao vivo'...")
                button.click()
                time.sleep(3)
                
                logger.info("✅ Botão clicado com sucesso!")
                return True
                
            except Exception as e:
                logger.error(f"❌ Erro na tentativa {attempt}: {e}")
                if attempt < max_retries:
                    time.sleep(5)
                    self.driver.refresh()
                    time.sleep(5)
                    self.click_streaming_help_and_complete()
                    time.sleep(2)
        
        return False
    
    def enable_auto_start(self):
        """
        Ativa a opção "Ativar o início automático" nas configurações avançadas
        Isso faz com que a live inicie automaticamente quando detectar o stream
        """
        if not self.driver:
            return False
        
        try:
            logger.info("🔧 Tentando ativar 'Início automático'...")
            
            # Procura o toggle de início automático
            toggle_selectors = [
                "//label[contains(text(), 'Ativar o início automático')]",
                "//label[contains(text(), 'Enable automatic start')]",
                "//input[@type='checkbox' and contains(@aria-label, 'início automático')]",
                "//input[@type='checkbox' and contains(@aria-label, 'automatic start')]",
            ]
            
            for selector in toggle_selectors:
                try:
                    wait = WebDriverWait(self.driver, 5)
                    toggle = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    # Verifica se já está ativado
                    if toggle.is_selected() or "checked" in toggle.get_attribute("class").lower():
                        logger.info("✅ 'Início automático' já está ativado")
                        return True
                    # Clica para ativar
                    toggle.click()
                    logger.info("✅ 'Início automático' ativado")
                    return True
                except TimeoutException:
                    continue
            
            logger.warning("⚠️  Toggle de início automático não encontrado (pode já estar ativado)")
            return True
            
        except Exception as e:
            logger.warning(f"⚠️  Erro ao ativar início automático: {e}")
            return False
    
    def start_live_automation(self, broadcast_id, enable_auto_start=True, wait_for_login=True):
        """
        Método completo para iniciar live via automação web
        
        Args:
            broadcast_id: ID do broadcast
            enable_auto_start: Se True, tenta ativar início automático
            wait_for_login: Se True, aguarda indefinidamente até fazer login
        
        Returns:
            True se sucesso, False caso contrário
        """
        try:
            # 1. Configura driver
            if not self._setup_driver():
                return False
            
            # 2. Faz login (ou verifica se já está logado)
            if not self.login_youtube():
                if wait_for_login:
                    logger.warning("⚠️  Login necessário")
                    logger.info("💡 O navegador está aberto. Por favor, faça login.")
                    logger.info("💡 O script continuará automaticamente quando você fizer login.")
                    logger.info("💡 Pressione Ctrl+C no terminal se quiser cancelar.")
                    # Tenta novamente após aguardar mais tempo
                    logger.info("💡 Aguardando mais 2 minutos para login...")
                    time.sleep(120)
                    if not self.login_youtube():
                        logger.error("❌ Ainda não está logado. Execute novamente após fazer login.")
                        return False
                else:
                    logger.warning("⚠️  Não foi possível fazer login automaticamente")
                    logger.info("💡 Você precisa estar logado no YouTube no navegador")
                    logger.info("💡 Abra o navegador manualmente e faça login, depois execute novamente")
                    return False
            
            # 3. Navega para a live
            if not self.go_to_live_stream(broadcast_id):
                return False
            
            # 4. Ativa início automático (se solicitado)
            if enable_auto_start:
                self.enable_auto_start()
            
            # 5. Clica no botão "Transmitir ao vivo"
            if self.click_go_live_button():
                logger.info("✅ Live iniciada via automação web!")
                return True
            else:
                logger.error("❌ Falha ao clicar no botão 'Transmitir ao vivo'")
                return False
                
        except Exception as e:
            logger.error(f"❌ Erro na automação: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Mantém o navegador aberto por alguns segundos para verificar
            if self.driver:
                logger.info("⏳ Mantendo navegador aberto por 10 segundos para verificação...")
                time.sleep(10)
    
    def close(self):
        """Fecha o navegador"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("✅ Navegador fechado")
            except:
                pass
            finally:
                self.driver = None
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()

