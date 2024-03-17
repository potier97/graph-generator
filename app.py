import json
import pandas as pd
import matplotlib.pyplot as plt

# Cargar los datos JSON desde el archivo
with open('request_log.json', 'r') as file:
    datos = json.load(file)


# Convertir los datos en un DataFrame de Pandas
df = pd.DataFrame(datos)

df.to_csv('datos.csv', index=False)

# Contar el número de solicitudes exitosas y fallidas
solicitudes_exitosas = df[df['status_code'] == 200].shape[0]
solicitudes_fallidas = df[df['status_code'] == 401].shape[0]

# Verificar si hay usuarios duplicados
usuarios_duplicados = df.duplicated(subset=['usuario']).any()


# Cargar los datos del archivo CSV
df_csv = pd.read_csv('usuarios.csv', sep=';', header=0)

usuarios_salud = df_csv['usuario']
print(usuarios_salud)

df_json_salud = df[df['usuario'].isin(usuarios_salud)]

usuarios_respuestas = dict(zip(df_json_salud['usuario'], df_json_salud['status_code']))
print(usuarios_respuestas)

resultados = {}
for usuario, respuesta in usuarios_respuestas.items():
    if respuesta == 200:
        resultados[usuario] = 'Correcto'
    else:
        resultados[usuario] = 'Incorrecto'

print(resultados)

if usuarios_duplicados:
    print("Hay usuarios duplicados en las solicitudes.")
else:
    print("No hay usuarios duplicados en las solicitudes.")

print("Solicitudes exitosas:", solicitudes_exitosas)
print("Solicitudes fallidas:", solicitudes_fallidas)

# Calcular porcentajes
total_solicitudes = solicitudes_exitosas + solicitudes_fallidas
porcentaje_exitosas_porcentaje = (solicitudes_exitosas / total_solicitudes) * 100
porcentaje_exitosas_porcentaje = (solicitudes_fallidas / total_solicitudes) * 100

plt.bar(['Exitosas', 'Fallidas'], [solicitudes_exitosas, solicitudes_fallidas])
plt.xlabel('Tipo de solicitud')
plt.ylabel('Número de solicitudes')
plt.title('Solicitudes HTTP')

plt.savefig('solicitudes_http.png')
plt.close()

# Diagrama de torta
plt.figure(figsize=(8, 6))  # Definir el tamaño de la figura
plt.pie([solicitudes_exitosas, solicitudes_fallidas], labels=['Exitosas', 'Fallidas'], autopct='%1.1f%%', startangle=90)
plt.title('Porcentaje de solicitudes HTTP')

# Agregar un cuadro alrededor del gráfico
plt.gca().set_aspect('equal')  # Esto asegura que el gráfico de torta tenga forma de círculo
plt.tight_layout(pad=3)  # Ajusta el espacio entre el gráfico y el borde de la figura
plt.gca().legend(loc='upper right', fontsize='medium', frameon=True, edgecolor='black')  # Agregar leyenda

# Guardar el gráfico como una imagen con un título y un marco
plt.savefig('porcentaje_solicitudes_http.png', bbox_inches='tight', pad_inches=0.5)

# Cierra la figura para liberar memoria
plt.close()

# Crear un gráfico de barras para visualizar los resultados de la validación
df_resultados = pd.DataFrame(resultados.items(), columns=['Usuario', 'Validación'])

colors = []
for index, row in df_resultados.iterrows():
    if row['Validación'] == 'Correcto':
        colors.append(['lightgreen'] * len(df_resultados.columns))
    else:
        colors.append(['lightcoral'] * len(df_resultados.columns))

# Crear una figura y ejes de tamaño apropiado
fig, ax = plt.subplots(figsize=(8, 6))

# Desactivar los ejes
ax.axis('off')

# Crear la tabla
tabla = ax.table(cellText=df_resultados.values,
                 colLabels=df_resultados.columns,
                 cellLoc='center',
                 loc='center',
                 cellColours=colors)

tabla.auto_set_font_size(False)
tabla.set_fontsize(12)

# Guardar la tabla como una imagen
plt.tight_layout()
plt.savefig('validacion_usuarios_tabla.png', bbox_inches='tight', pad_inches=0.5)