import yaml

class Pregunta:
    def __init__(self, title: str, prompt: str, hints: list[str], tags: list[str]):
        self.title = title
        self.prompt = prompt
        self.hints = hints
        self.tags = tags

    def to_dict(self) -> dict:
        """Convierte el objeto a un diccionario compatible con el archivo YAML."""
        return {
            "title": self.title,
            "prompt": self.prompt,
            "hints": self.hints,
            "tags": self.tags
        }


def cargar_preguntas(filepath: str, preguntas: list[Pregunta]) -> None:
    """
    Carga una lista de objetos Pregunta en un archivo YAML.
    Si el archivo ya existe, añade las preguntas al contenido existente.
    """
    datos_existentes = []
    
    # Leer contenido previo si el archivo existe
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            contenido = yaml.safe_load(file)
            if isinstance(contenido, list):
                datos_existentes = contenido
    except FileNotFoundError:
        pass  # El archivo se creará desde cero

    # Convertir las nuevas preguntas a diccionarios
    nuevos_datos = [p.to_dict() for p in preguntas]
    datos_totales = datos_existentes + nuevos_datos

    # Guardar todo en el archivo YAML
    with open(filepath, "w", encoding="utf-8") as file:
        yaml.dump(
            datos_totales,
            file,
            allow_unicode=True,
            sort_keys=False,
            default_flow_style=False
        )


# --- Ejemplo de uso ---
if __name__ == "__main__":
    # 1. Crear objetos Pregunta
    p1 = Pregunta(
        title="Suma dos números",
        prompt="Escribe `suma(a, b)` que devuelva a + b.",
        hints=["Usa operadores aritméticos", "Devuelve el resultado"],
        tags=["funciones", "aritmética"]
    )
    
    p2 = Pregunta(
        title="Es número par",
        prompt="Escribe `es_par(n)` que devuelva `True` si n es par y `False` si es impar.",
        hints=["Usa el operador módulo `%`", "Compara la resta del módulo con 0"],
        tags=["funciones", "condicionales", "booleans"]
    )

    # 2. Cargar las preguntas en el YAML
    lista_preguntas = [p1, p2]
    cargar_preguntas("problems.yaml", lista_preguntas)
    print("Preguntas guardadas correctamente en problems.yaml")