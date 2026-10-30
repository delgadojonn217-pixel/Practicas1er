# Paso 1: Crear el conjunto de datos

precio <- c(
  95000, 119000, 124800, 135000, 142800, 145000, 159000,
  165000, 182000, 183000, 200000, 211000, 215000, 219000
)

pies_cuadrados <- c(
  1926, 2069, 1720, 1396, 1706, 1847, 1950,
  2323, 2285, 3752, 2300, 2525, 3800, 1740
)

antiguedad <- c(
  30, 40, 30, 15, 32, 38, 27,
  30, 26, 35, 18, 17, 40, 12
)


# Paso 2: Crear el Data Frame

datos_casas <- data.frame(
  precio,
  pies_cuadrados,
  antiguedad
)

# Mostrar los datos
print(datos_casas)


# Paso 3: Ajustar el modelo de regresión múltiple

modelo_multi <- lm(
  precio ~ pies_cuadrados + antiguedad,
  data = datos_casas
)


# Paso 4: Mostrar los coeficientes del modelo

print(modelo_multi)


# Paso 5: Mostrar el resumen estadístico

print(summary(modelo_multi))


# Paso 6: Pronosticar el precio de una nueva casa

# Casa de 2000 pies cuadrados y 10 años de antigüedad
nueva_casa <- data.frame(
  pies_cuadrados = 2000,
  antiguedad = 10
)

precio_estimado <- predict(
  modelo_multi,
  newdata = nueva_casa
)


# Paso 7: Mostrar el precio pronosticado

print(precio_estimado)

# Mostrarlo con dos decimales
cat(sprintf("Precio estimado: %.2f\n", precio_estimado))
