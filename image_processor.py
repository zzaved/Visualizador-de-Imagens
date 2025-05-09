from PIL import Image, ImageOps, ImageFilter, ImageEnhance
import numpy as np
import cv2

def grayscale(image):
    """
    Converte a imagem para escala de cinza.
    
    Args:
        image: Objeto PIL Image
    
    Returns:
        Imagem em escala de cinza
    """
    return ImageOps.grayscale(image).convert('RGB')

def invert_colors(image):
    """
    Inverte as cores da imagem.
    
    Args:
        image: Objeto PIL Image
    
    Returns:
        Imagem com cores invertidas
    """
    return ImageOps.invert(image)

def increase_contrast(image, factor=1.5):
    """
    Aumenta o contraste da imagem.
    
    Args:
        image: Objeto PIL Image
        factor: Fator de contraste 
               (1.0 = sem alteração, 
                < 1.0 = redução de contraste, 
                > 1.0 = aumento de contraste)
    
    Returns:
        Imagem com contraste ajustado
    """
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def blur_image(image, amount=2):
    """
    Aplica desfoque (blur) na imagem.
    
    Args:
        image: Objeto PIL Image
        amount: Intensidade do desfoque
    
    Returns:
        Imagem com desfoque aplicado
    """
    return image.filter(ImageFilter.GaussianBlur(radius=amount))

def sharpen_image(image, amount=5):
    """
    Aumenta a nitidez da imagem.
    
    Args:
        image: Objeto PIL Image
        amount: Intensidade da nitidez
    
    Returns:
        Imagem com nitidez aumentada
    """
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(amount / 2.0)  # Dividimos por 2 para tornar o efeito mais suave

def edge_detection(image, threshold1=100, threshold2=200):
    """
    Aplica detecção de bordas na imagem.
    
    Args:
        image: Objeto PIL Image
        threshold1: Parâmetro de ajuste de sensibilidade (quanto maior, menos sensível)
        threshold2: Parâmetro de ajuste de intensidade (quanto maior, bordas mais fortes)
    
    Returns:
        Imagem com bordas detectadas 
    """
    # Converter para escala de cinza
    gray_img = image.convert('L')
    
    # Aplicar filtro de detecção de bordas do PIL
    edges = gray_img.filter(ImageFilter.FIND_EDGES)
    
    # Ajustar contraste com base no threshold2
    enhancer = ImageEnhance.Contrast(edges)
    contrast_factor = threshold2 / 128.0  # Normaliza para que 200 seja ~1.5x o contraste
    edges = enhancer.enhance(contrast_factor)
    
    # Ajustar brilho (torna bordas mais ou menos visíveis) com base no threshold1
    enhancer = ImageEnhance.Brightness(edges)
    brightness_factor = 1.0 - (threshold1 / 255.0)  # Quanto menor o threshold1, mais bordas aparecem
    edges = enhancer.enhance(brightness_factor)
    
    # Converter de volta para RGB
    return edges.convert('RGB')

def rotate_image(image, angle):
    """
    Rotaciona a imagem por um ângulo específico.
    
    Args:
        image: Objeto PIL Image
        angle: Ângulo de rotação em graus
    
    Returns:
        Imagem rotacionada
    """
    return image.rotate(angle, resample=Image.BICUBIC, expand=True)

def resize_image(image, scale_factor):
    """
    Redimensiona a imagem por um fator de escala.
    
    Args:
        image: Objeto PIL Image
        scale_factor: Fator de escala (1.0 = tamanho original)
    
    Returns:
        Imagem redimensionada
    """
    width, height = image.size
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    return image.resize((new_width, new_height), Image.LANCZOS)