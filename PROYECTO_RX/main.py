import dash

from modulos.interfaz import (
    crear_layout,
    registrar_callbacks
)

from modulos.teoria_rx import (
    registrar_callbacks as registrar_callbacks_teoria
)

from modulos.procesamiento import (
    registrar_callbacks as registrar_callbacks_procesamiento
)

from modulos.actividades import (
    registrar_callbacks as registrar_callbacks_actividades
)

from modulos.analisis import (
    registrar_callbacks as registrar_callbacks_analisis
)


app = dash.Dash(
    __name__,
    external_stylesheets=[
        "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"
    ],
    title="Plataforma Educativa de Rayos X",
    suppress_callback_exceptions=True
)
server = app.server

app.layout = crear_layout()


registrar_callbacks(app)

registrar_callbacks_teoria(app)

registrar_callbacks_procesamiento(app)

registrar_callbacks_actividades(app)

registrar_callbacks_analisis(app)

if __name__ == "__main__":
    app.run(debug=True)
