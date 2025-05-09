import streamlit as st
from PIL import Image
import numpy as np
import io
from image_processor import (
    grayscale,
    invert_colors,
    increase_contrast,
    blur_image,
    sharpen_image,
    edge_detection,
    rotate_image,
    resize_image
)

def main():
    st.set_page_config(
        page_title="Visualizador de Imagens",
        page_icon="🖼️",
        layout="wide"
    )
    
    # Inicialização de variáveis de estado da sessão
    if 'rotation_angle' not in st.session_state:
        st.session_state.rotation_angle = 0
    
    # Título principal
    st.title("Visualizador de Imagens com Filtros")
    
    # Configuração do layout principal
    col1, col2 = st.columns(2)
    
    # Caixas para as imagens com contorno
    with col1:
        st.subheader("📷 Imagem Original")
        with st.container(border=True):
            original_image_container = st.container()
        original_info = st.empty()  # Para mostrar dimensões
    
    with col2:
        st.subheader("✨ Imagem com Filtros Aplicados")
        with st.container(border=True):
            processed_image_container = st.container()
        processed_info = st.empty()  # Para mostrar dimensões
    
    # Upload da imagem (mostrado nas caixas se não houver imagem)
    if 'image' not in st.session_state:
        with original_image_container:
            st.info("Insira uma imagem para começar")
            uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
            
            if uploaded_file is not None:
                try:
                    image = Image.open(uploaded_file)
                    
                    # Converter para RGB (caso seja RGBA)
                    if image.mode == 'RGBA':
                        image = image.convert('RGB')
                    
                    # Guardar a imagem na sessão
                    st.session_state.image = image
                    st.session_state.filename = uploaded_file.name
                    st.rerun()  # Recarregar a página com a imagem
                    
                except Exception as e:
                    st.error(f"Erro ao processar a imagem: {e}")
                    st.info("Por favor, certifique-se de que o arquivo é uma imagem válida.")
    
    # Menu lateral para filtros e transformações
    st.sidebar.title("Filtros e Transformações")
    
    # Se tivermos uma imagem, mostrar os controles
    if 'image' in st.session_state:
        image = st.session_state.image
        
        # Seção de ajustes básicos
        st.sidebar.markdown("### 🎨 Ajustes Básicos")
        apply_grayscale = st.sidebar.checkbox("🔲 Escala de Cinza")
        apply_invert = st.sidebar.checkbox("🔄 Inversão de Cores")
        
        apply_contrast = st.sidebar.checkbox("🌓 Ajuste de Contraste")
        if apply_contrast:
            contrast_level = st.sidebar.slider("Nível de Contraste", 0, 100, 50)
            contrast_factor = 0.5 + (contrast_level / 50.0)  # Mapeia 0-100 para 0.5-2.5
        
        # Seção de efeitos
        st.sidebar.markdown("### 🖌️ Efeitos")
        
        apply_blur = st.sidebar.checkbox("🌫️ Desfoque (Blur)")
        if apply_blur:
            blur_amount = st.sidebar.slider("Intensidade do Desfoque", 0, 10, 2)
        else:
            blur_amount = 0
        
        apply_sharpen = st.sidebar.checkbox("✏️ Nitidez (Sharpen)")
        if apply_sharpen:
            sharpen_amount = st.sidebar.slider("Intensidade da Nitidez", 0, 10, 5)
        else:
            sharpen_amount = 0
        
        apply_edge = st.sidebar.checkbox("🧩 Detector de Bordas")
        if apply_edge:
            edge_lower = st.sidebar.slider("Sensibilidade de Detecção", 0, 255, 100)
            edge_upper = st.sidebar.slider("Intensidade das Bordas", 0, 255, 200)
        
        # Seção de transformações
        st.sidebar.markdown("### 📐 Transformações")
        
        # Rotação
        apply_rotation = st.sidebar.checkbox("🔄 Rotação")
        if apply_rotation:
            col1, col2 = st.sidebar.columns(2)
            with col1:
                if st.button("↺ Girar 90° Anti-horário"):
                    st.session_state.rotation_angle = (st.session_state.rotation_angle - 90) % 360
                    st.rerun()  # Recarregar para aplicar rotação
            with col2:
                if st.button("↻ Girar 90° Horário"):
                    st.session_state.rotation_angle = (st.session_state.rotation_angle + 90) % 360
                    st.rerun()  # Recarregar para aplicar rotação
            
            # Exibir ângulo atual
            st.sidebar.write(f"Ângulo atual: {st.session_state.rotation_angle}°")
            rotation_angle = st.session_state.rotation_angle
        else:
            rotation_angle = 0
        
        # Redimensionamento
        apply_resize = st.sidebar.checkbox("🔍 Redimensionar")
        if apply_resize:
            # Obter dimensões originais
            original_width, original_height = image.size
            st.sidebar.write(f"Tamanho original: {original_width} × {original_height} pixels")
            
            # Slider de porcentagem
            resize_percentage = st.sidebar.slider("Porcentagem do Tamanho Original", 10, 200, 100)
            
            # Calcular e exibir novo tamanho
            new_width = int(original_width * resize_percentage / 100)
            new_height = int(original_height * resize_percentage / 100)
            st.sidebar.write(f"Novo tamanho: {new_width} × {new_height} pixels")
        else:
            resize_percentage = 100
        
        # Botão para limpar e começar novamente
        st.sidebar.markdown("---")
        if st.sidebar.button("🗑️ Limpar e Recomeçar"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        # Mostrar imagem original
        with original_image_container:
            st.image(image, use_container_width=True)
        
        # Mostrar informações da imagem original
        width, height = image.size
        original_info.write(f"Dimensões: {width} × {height} pixels")
        
        # Processar a imagem
        processed_image = image.copy()
        
        # Aplicar filtros selecionados
        if apply_grayscale:
            processed_image = grayscale(processed_image)
        
        if apply_invert:
            processed_image = invert_colors(processed_image)
        
        if apply_contrast:
            processed_image = increase_contrast(processed_image, factor=contrast_factor)
        
        if apply_blur and blur_amount > 0:
            processed_image = blur_image(processed_image, blur_amount)
        
        if apply_sharpen and sharpen_amount > 0:
            processed_image = sharpen_image(processed_image, sharpen_amount)
        
        if apply_edge:
            processed_image = edge_detection(processed_image, threshold1=edge_lower, threshold2=edge_upper)
        
        # Aplicar transformações
        if apply_rotation and rotation_angle != 0:
            processed_image = rotate_image(processed_image, rotation_angle)
        
        if apply_resize and resize_percentage != 100:
            processed_image = resize_image(processed_image, resize_percentage / 100.0)
        
        # Mostrar imagem processada
        with processed_image_container:
            st.image(processed_image, use_container_width=True)
        
        # Mostrar informações da imagem processada
        p_width, p_height = processed_image.size
        processed_info.write(f"Dimensões: {p_width} × {p_height} pixels")
        
        # Botão para download da imagem processada
        st.write("## 💾 Salvar Resultado")
        if st.button("Salvar Imagem Processada"):
            buf = io.BytesIO()
            processed_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            # Gerar nome para o arquivo processado
            original_filename = st.session_state.filename
            name_parts = original_filename.split('.')
            if len(name_parts) > 1:
                new_filename = f"{name_parts[0]}_processado.png"
            else:
                new_filename = "imagem_processada.png"
            
            st.download_button(
                label="Download da Imagem",
                data=byte_im,
                file_name=new_filename,
                mime="image/png"
            )

if __name__ == "__main__":
    main()