from itertools import cycle
import numpy as np
import cv2 as cv
import os

WIDTH = 1400
MAX_VALUE = 1 << 8
ORG = (20, 30), (20, 65)
FONT_FACE = cv.FONT_HERSHEY_PLAIN
FONT_SCALE = 2
COLOR = 255
THICKNESS = 3


def describe_image(image: np.ndarray, b: int) -> None:
    """Escreve um texto com as informações de quantização
    de uma imagem digital, além de quantas cores (pixels)
    únicos existem na mesma.

    Parameters
    ----------
    image : np.array
        Um array de numpy de shape (n,m), onde n é a amostragem da imagem
    b : int
        Um número inteiro especificando o número de bits
    """
    cv.putText(
        image,
        f"CORES: {np.unique(image).shape[0]}",
        ORG[0],
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )

    cv.putText(
        image,
        f"BITS: {b}",
        ORG[1],
        FONT_FACE,
        FONT_SCALE,
        COLOR,
        THICKNESS,
    )


def get_quantization(image: np.ndarray, b: int) -> np.ndarray:
    """Quantiza uma imagem digital para um número
    de bits especificado de acordo como parâmetro
    b.

    Parameters
    ----------
    image : np.array
        Um array de numpy de shape (n,m), onde n é a amostragem da imagem
    b : int
        Um número inteiro especificando o número de bits

    Returns
    -------
    np.array
        Retorna um array numpy com as cores quantizadas
    """
    n_colors = 1 << b
    i_min = image.min()
    i_max = image.max()
    color_rate = MAX_VALUE / n_colors
    quantized = (n_colors - 1) * ((image - i_min) / (i_max - i_min))
    result_image = np.round(quantized) * color_rate
    describe_image(result_image, b)

    return result_image.astype("uint8")


if __name__ == "__main__":

    curdir = os.path.dirname(__file__)
    image = cv.imread(os.path.join(curdir, "images", "tucano.jpg"), cv.IMREAD_GRAYSCALE)
    im, _range = cycle([image]), range(1, 9)
    quantized_images = map(get_quantization, im, _range)

    shape = 3, 3, *image.shape
    images = *quantized_images, image
    cv.putText(image, "ORIGINAL", ORG[1], FONT_FACE, FONT_SCALE + 1, COLOR, THICKNESS)

    image_grid = np.vstack([np.hstack(arr) for arr in np.reshape(images, shape)])
    r = WIDTH / image_grid.shape[1]
    cv.imwrite(os.path.join(curdir, "images", "grid.jpg"), image_grid)
    result = cv.resize(image_grid, None, fx=r, fy=r)

    cv.imshow("Image Grid - Quantization", result)
    cv.waitKey(0)
