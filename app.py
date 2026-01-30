from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


def get_country_code(country_name):
    # Diccionario rápido para los más importantes, puedes seguir aumentándolo
    mapping = {
        'España': 'es', 'Spain': 'es',
        'Argentina': 'ar',
        'Francia': 'fr', 'France': 'fr',
        'Alemania': 'de', 'Germany': 'de',
        'Portugal': 'pt',
        'Brasil': 'br', 'Brazil': 'br',
        'Inglaterra': 'gb-eng', 'England': 'gb-eng',
        'Paises Bajos': 'nl', 'Netherlands': 'nl',
        'Países Bajos': 'nl', 'Netherlands': 'nl',
        'Japón': 'jp', 'Japan': 'jp',
        'Bélgica': 'be', 'Belgium': 'be',
        'Turkey': 'tr', 'Turquía': 'tr', # Agregué Turquía que te fallaba
        'Ukraine': 'ua', 'Ucrania': 'ua',
        'Mexico': 'mx', 'México': 'mx', 
        'Switzerland': 'ch', 'Suiza': 'ch',
        'Uruguay': 'uy', 'Uruguaya': 'uy',
        'Estados Unidos': 'us', 'USA': 'us', 'United States': 'us',
        'Corea del Sur': 'kr', 'South Korea': 'kr', 'Korea, South': 'kr',
        'Eslovaquia': 'sk', 'Slovakia': 'sk', 'Slovak Republic': 'sk'
    }
    return mapping.get(country_name, country_name.lower()[:2])

# Registramos la función para que el HTML la pueda usar
app.jinja_env.globals.update(get_country_code=get_country_code)

@app.route('/')
def home():
    # Aquí es donde después cargarás tus resultados
    return render_template('index.html')

@app.route('/predicciones')
def predicciones():
    df = pd.read_csv('datasets/predicciones.csv')
    cols_porcentaje = ['Win Group', 'R32', 'Quarters', 'Semis', 'Final', 'Champion']
    for col in cols_porcentaje:
        df[col] = df[col].str.replace('%', '').astype(float)
    max_champion = df['Champion'].max()
    df['Ancho_Visual'] = (df['Champion'] / max_champion) * 100
    return render_template('predicciones.html', predicciones=df.to_dict(orient='records'))

@app.route('/grupos')
def grupos():
    df_partidos = pd.read_csv('datasets/grupos_mundial.csv')
    df_probs = pd.read_csv('datasets/clasificados.csv')
    df_final = pd.merge(df_partidos, df_probs, left_on='grupo', right_on='Grupo', how='left')
    grupos = df_final.to_dict(orient='records')
    return render_template('grupos.html', grupos=grupos)

@app.route('/goleadores')
def goleadores():
    df = pd.read_csv('datasets/goleadores.csv')
    df['foto_path'] = 'jugadores/' + df['scorer'].str.strip() + '.png'
    datos_goleadores = df.to_dict(orient='records')
    return render_template('goleadores.html', goleadores=datos_goleadores)

@app.route('/tarjetas')
def tarjetas():
    df = pd.read_csv('datasets/tarjetas.csv')
    datos_tarjetas = df.to_dict(orient='records')
    return render_template('tarjetas.html', tarjetas=datos_tarjetas)

@app.route('/muerte')
def muerte():
    df = pd.read_csv('datasets/dificultad.csv')
    datos_dificultad = df.to_dict(orient='records')
    return render_template('muerte.html', muerte=datos_dificultad)

@app.route('/arqueros')
def arqueros():
    df = pd.read_csv('datasets/arqueros.csv')

    # Ordenamos por vallas invictas proyectadas (Top 10)
    arqueros = df.sort_values(by='Expected_Clean_Sheets', ascending=False).head(10).to_dict(orient='records')
    for p in arqueros:
        # Clasificación personalizada
        if p['age_2026'] >= 36:
            p['categoria'] = 'Leyenda'
            p['color_cat'] = '#B8860B' # Dorado oscuro
        else:
            p['categoria'] = 'Prime'
            p['color_cat'] = '#4A773C' # Verde

    return render_template('arqueros.html', arqueros=arqueros)

if __name__ == '__main__':
    app.run(debug=True)