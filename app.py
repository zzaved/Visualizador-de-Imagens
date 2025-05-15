import streamlit as st  # Importa a biblioteca Streamlit para criar interfaces web interativas
from PIL import Image  # Importa a biblioteca Pillow para processamento de imagens
import numpy as np  # Importa NumPy para operações em arrays (usado em algumas funções de processamento)
import io  # Importa a biblioteca io para manipulação de entrada/saída de bytes (usado para download)

# Importa todas as funções de processamento de imagem do arquivo image_processor.py
from image_processor import (
    grayscale,           # Função para converter para escala de cinza
    invert_colors,       # Função para inverter cores da imagem
    increase_contrast,   # Função para ajustar contraste
    blur_image,          # Função para aplicar desfoque
    sharpen_image,       # Função para aumentar nitidez
    edge_detection,      # Função para detectar bordas
    rotate_image,        # Função para rotacionar imagem
    resize_image         # Função para redimensionar imagem
)

def main():
    # Configura as propriedades da página Streamlit (título, ícone e layout)
    st.set_page_config(
        page_title="Visualizador de Imagens",
        page_icon="🖼️",
        layout="wide"  # Layout amplo para melhor visualização das imagens
    )
    
    # Inicialização de variáveis de estado da sessão
    # Estas variáveis persistem entre recarregamentos da página
    if 'rotation_angle' not in st.session_state:
        st.session_state.rotation_angle = 0  # Inicializa o ângulo de rotação como 0 graus
    
    # Título principal do aplicativo
    st.title("Visualizador de Imagens com Filtros")
    
    # Configura o layout principal dividindo a tela em duas colunas
    col1, col2 = st.columns(2)
    
    # Caixa para a imagem original com contorno
    with col1:
        st.subheader("📷 Imagem Original")
        with st.container(border=True):  # Cria um contêiner com borda para a imagem
            original_image_container = st.container()  # Container para imagem original
        original_info = st.empty()  # Placeholder para mostrar dimensões da imagem original
    
    # Caixa para a imagem processada com contorno
    with col2:
        st.subheader("✨ Imagem com Filtros Aplicados")
        with st.container(border=True):  # Cria um contêiner com borda para a imagem processada
            processed_image_container = st.container()  # Container para imagem processada
        processed_info = st.empty()  # Placeholder para mostrar dimensões da imagem processada
    
    # Verifica se já existe uma imagem na sessão, senão mostra o uploader
    if 'image' not in st.session_state:
        with original_image_container:
            st.info("Insira uma imagem para começar")
            # Componente para upload de arquivos, limitado a formatos de imagem
            uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
            
            if uploaded_file is not None:
                try:
                    # Tenta abrir a imagem com a biblioteca Pillow
                    image = Image.open(uploaded_file)
                    
                    # Converte a imagem para RGB caso esteja em RGBA (com transparência)
                    # Isso é necessário pois alguns filtros não funcionam bem com RGBA
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    
                    # Armazena a imagem e nome do arquivo na sessão para uso posterior
                    st.session_state.image = image
                    st.session_state.filename = uploaded_file.name
                    st.rerun()  # Recarrega a página para mostrar a imagem e os controles
                    
                except Exception as e:
                    # Tratamento de erros ao processar a imagem
                    st.error(f"Erro ao processar a imagem: {e}")
                    st.info("Por favor, certifique-se de que o arquivo é uma imagem válida.")
    
    # Menu lateral para filtros e transformações
    st.sidebar.title("Filtros e Transformações")
    
    # Só mostra os controles se houver uma imagem carregada
    if 'image' in st.session_state:
        # Recupera a imagem da sessão
        image = st.session_state.image
        
        # ---------- SEÇÃO DE AJUSTES BÁSICOS ----------
        st.sidebar.markdown("### 🎨 Ajustes Básicos")
        
        # Checkbox para ativar/desativar escala de cinza
        apply_grayscale = st.sidebar.checkbox("🔲 Escala de Cinza")
        
        # Checkbox para ativar/desativar inversão de cores
        apply_invert = st.sidebar.checkbox("🔄 Inversão de Cores")
        
        # Controle de contraste com slider
        apply_contrast = st.sidebar.checkbox("🌓 Ajuste de Contraste")
        if apply_contrast:
            # Slider de 0 a 100 para ajustar o nível de contraste
            contrast_level = st.sidebar.slider("Nível de Contraste", 0, 100, 50)
            # Converte o valor do slider (0-100) para um fator de contraste (0.5-2.5)
            contrast_factor = 0.5 + (contrast_level / 50.0)
        
        # ---------- SEÇÃO DE EFEITOS ----------
        st.sidebar.markdown("### 🖌️ Efeitos")
        
        # Controle de desfoque (blur)
        apply_blur = st.sidebar.checkbox("🌫️ Desfoque (Blur)")
        if apply_blur:
            # Slider para controlar a intensidade do desfoque
            blur_amount = st.sidebar.slider("Intensidade do Desfoque", 0, 10, 2)
        else:
            blur_amount = 0  # Define como 0 se não aplicar
        
        # Controle de nitidez (sharpen)
        apply_sharpen = st.sidebar.checkbox("✏️ Nitidez (Sharpen)")
        if apply_sharpen:
            # Slider para controlar a intensidade da nitidez
            sharpen_amount = st.sidebar.slider("Intensidade da Nitidez", 0, 10, 5)
        else:
            sharpen_amount = 0  # Define como 0 se não aplicar
        
        # Controle de detecção de bordas
        apply_edge = st.sidebar.checkbox("🧩 Detector de Bordas")
        if apply_edge:
            # Sliders para ajustar os parâmetros da detecção de bordas
            edge_lower = st.sidebar.slider("Sensibilidade de Detecção", 0, 255, 100)
            edge_upper = st.sidebar.slider("Intensidade das Bordas", 0, 255, 200)
        
        # ---------- SEÇÃO DE TRANSFORMAÇÕES ----------
        st.sidebar.markdown("### 📐 Transformações")
        
        # Controle de rotação
        apply_rotation = st.sidebar.checkbox("🔄 Rotação")
        if apply_rotation:
            # Cria duas colunas para os botões de rotação
            col1, col2 = st.sidebar.columns(2)
            with col1:
                # Botão para rotacionar 90° no sentido anti-horário
                if st.button("↺ Girar 90° Anti-horário"):
                    # Atualiza o ângulo na sessão (mantém entre 0-359°)
                    st.session_state.rotation_angle = (st.session_state.rotation_angle - 90) % 360
                    st.rerun()  # Recarrega para aplicar a rotação
            with col2:
                # Botão para rotacionar 90° no sentido horário
                if st.button("↻ Girar 90° Horário"):
                    # Atualiza o ângulo na sessão (mantém entre 0-359°)
                    st.session_state.rotation_angle = (st.session_state.rotation_angle + 90) % 360
                    st.rerun()  # Recarrega para aplicar a rotação
            
            # Exibe o ângulo atual de rotação
            st.sidebar.write(f"Ângulo atual: {st.session_state.rotation_angle}°")
            rotation_angle = st.session_state.rotation_angle
        else:
            rotation_angle = 0  # Sem rotação se o checkbox não estiver marcado
        
        # Controle de redimensionamento
        apply_resize = st.sidebar.checkbox("🔍 Redimensionar")
        if apply_resize:
            # Obtém as dimensões originais da imagem
            original_width, original_height = image.size
            st.sidebar.write(f"Tamanho original: {original_width} × {original_height} pixels")
            
            # Slider para ajustar a porcentagem do tamanho
            resize_percentage = st.sidebar.slider("Porcentagem do Tamanho Original", 10, 200, 100)
            
            # Calcula e exibe o novo tamanho em pixels
            new_width = int(original_width * resize_percentage / 100)
            new_height = int(original_height * resize_percentage / 100)
            st.sidebar.write(f"Novo tamanho: {new_width} × {new_height} pixels")
        else:
            resize_percentage = 100  # 100% = tamanho original
        
        # Botão para limpar e recomeçar
        st.sidebar.markdown("---")  # Linha horizontal para separar
        if st.sidebar.button("🗑️ Limpar e Recomeçar"):
            # Remove todas as variáveis da sessão
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()  # Recarrega a página para o estado inicial
        
        # ---------- EXIBIÇÃO DA IMAGEM ORIGINAL ----------
        with original_image_container:
            # Mostra a imagem original (ajustada para preencher o container)
            st.image(image, use_container_width=True)
        
        # Mostra as dimensões da imagem original
        width, height = image.size
        original_info.write(f"Dimensões: {width} × {height} pixels")
        
        # ---------- PROCESSAMENTO DA IMAGEM ----------
        # Cria uma cópia da imagem original para não modificá-la
        processed_image = image.copy()
        
        # Aplica os filtros selecionados na ordem especificada
        # A ordem pode afetar o resultado final
        
        # 1. Filtro de escala de cinza
        if apply_grayscale:
            processed_image = grayscale(processed_image)
        
        # 2. Filtro de inversão de cores
        if apply_invert:
            processed_image = invert_colors(processed_image)
        
        # 3. Ajuste de contraste
        if apply_contrast:
            processed_image = increase_contrast(processed_image, factor=contrast_factor)
        
        # 4. Filtro de desfoque (blur)
        if apply_blur and blur_amount > 0:
            processed_image = blur_image(processed_image, blur_amount)
        
        # 5. Filtro de nitidez (sharpen)
        if apply_sharpen and sharpen_amount > 0:
            processed_image = sharpen_image(processed_image, sharpen_amount)
        
        # 6. Filtro de detecção de bordas
        if apply_edge:
            processed_image = edge_detection(processed_image, threshold1=edge_lower, threshold2=edge_upper)
        
        # Aplica transformações geométricas
        # 7. Rotação
        if apply_rotation and rotation_angle != 0:
            processed_image = rotate_image(processed_image, rotation_angle)
        
        # 8. Redimensionamento
        if apply_resize and resize_percentage != 100:
            processed_image = resize_image(processed_image, resize_percentage / 100.0)
        
        # ---------- EXIBIÇÃO DA IMAGEM PROCESSADA ----------
        with processed_image_container:
            # Mostra a imagem processada (ajustada para preencher o container)
            st.image(processed_image, use_container_width=True)
        
        # Mostra as dimensões da imagem processada
        p_width, p_height = processed_image.size
        processed_info.write(f"Dimensões: {p_width} × {p_height} pixels")
        
        # ---------- OPÇÃO DE DOWNLOAD ----------
        st.write("## 💾 Salvar Resultado")
        if st.button("Salvar Imagem Processada"):
            # Cria um buffer de bytes para salvar a imagem
            buf = io.BytesIO()
            processed_image.save(buf, format="PNG")  # Salva a imagem em formato PNG
            byte_im = buf.getvalue()  # Obtém os bytes da imagem
            
            # Gera um nome para o arquivo processado baseado no nome original
            original_filename = st.session_state.filename
            name_parts = original_filename.split('.')
            if len(name_parts) > 1:
                # Se o nome tiver extensão, adiciona "_processado" antes da extensão
                new_filename = f"{name_parts[0]}_processado.png"
            else:
                # Caso contrário, usa um nome padrão
                new_filename = "imagem_processada.png"
            
            # Cria um botão de download que permite salvar a imagem processada
            st.download_button(
                label="Download da Imagem",
                data=byte_im,
                file_name=new_filename,
                mime="image/png"
            )

# Verifica se este arquivo está sendo executado diretamente
# (não está sendo importado como um módulo)
if __name__ == "__main__":
    main()  # Chama a função principal para iniciar o aplicativo