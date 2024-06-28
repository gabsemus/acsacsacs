[app]

# Título do seu aplicativo
title = APPACS

# Nome do pacote
package.name = myapp

# Domínio do pacote (necessário para empacotamento android/ios)
package.domain = org.myapp

# Extensões de código-fonte a serem incluídas
source.include_exts = py,png,jpg,kv,atlas

# Arquivos de origem a serem incluídos (deixe vazio para incluir todos os arquivos)
source.include_patterns = assets/*,images/*.png

# Versionamento do aplicativo (método 1)
version = 0.1

# Requisitos do aplicativo
# separados por vírgulas, por exemplo: requirements = python3,kivy
requirements = python3,kivy,pandas

# Orientação suportada (uma das: landscape, portrait ou all)
orientation = portrait

# Permissões necessárias
# Permissões requeridas pelo aplicativo (lista separada por vírgulas).
# por exemplo: permissions = INTERNET,ACCESS_FINE_LOCATION
permissions = INTERNET

# O formato usado para empacotar o aplicativo para android
# (um dos: apk, aab, apk_expansion, universal)
android.package_type = apk

# Requisitos específicos para Android
# Habilitar serviços
android.services =

# Cor de fundo da tela de pré-carregamento (para nova cadeia de ferramentas android)
# Formatos suportados são: #RRGGBB, #AARRGGBB ou #RGB
android.presplash_color = #FFFFFF

# Caminho para o ícone
icon.filename = app/image/logo.png

# Caminho para a imagem de pré-carregamento
presplash.filename = app/image/logo.png

# Ícone adaptativo de fundo (cor ou caminho do arquivo)
android.adaptive_icon_background = app/image/logo.png

# Ícone adaptativo de primeiro plano (cor ou caminho do arquivo)
android.adaptive_icon_foreground = app/image/logo.png

# Indicar se o aplicativo deve ser em tela cheia ou não
fullscreen = 1

# API suportada pelo Android, geralmente é melhor deixar como está:
android.api = 28

# API mínima suportada pelo Android, padrão é 21
android.minapi = 21

# Versão do NDK Android a ser usada
android.ndk = 19b

# Usar a nova cadeia de ferramentas do Android (requer android.ndk = 19b ou superior)
android.new_toolchain = True

# Versão do SDK Android a ser usada
android.sdk = 26

# Versão das ferramentas de compilação Android a ser usada
android.build_tools_version = 28.0.3

# Filtros de ndk android, você deve colocar aqui a arquitetura suportada
android.ndk_api = 21

# Arquiteturas Android para as quais compilar
android.arch = armeabi-v7a,arm64-v8a

# Diretório onde o código-fonte está localizado
source.dir = .
