
x <- c(20,25,30,35,40)
y <- c(50,58,65,75,82)


# f0 - Calcular la media
media <- function(x) {
    return(sum(x) / length(x))
}


# f1 - Diferencia al cuadrado
diferencia_cuadrado <- function(x) {
    la_media <- media(x)
    la_diferencia <- 0

    for (i in x) {
        la_diferencia <- la_diferencia + (i - la_media) * (i - la_media)
    }

    return(la_diferencia)
}


# f2 - Diferencia XY
diferencia_xy <- function(x, y) {
    mediax <- media(x)
    mediay <- media(y)
    sumatoria <- 0

    for (i in seq_along(x)) {
        sumatoria <- sumatoria + (x[i] - mediax) * (y[i] - mediay)
    }

    return(sumatoria)
}


# f3 - Obtener b1
obtener_b1 <- function(x, y) {
    diferencia <- diferencia_xy(x, y)
    diferencia_cuadrados <- diferencia_cuadrado(x)

    return(diferencia / diferencia_cuadrados)
}


# f4 - Obtener b0
obtener_b0 <- function(x, y) {
    mediay <- media(y)
    mediax <- media(x)
    b1 <- obtener_b1(x, y)

    return(mediay - (b1 * mediax))
}


# f5 - Ecuacion de regresion lineal
obtener_y <- function(x, y, valor_x) {
    b0 <- obtener_b0(x, y)
    b1 <- obtener_b1(x, y)

    return(b0 + (b1 * valor_x))
}
