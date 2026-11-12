from POO import Pregunta, cargar_preguntas


def main():
    preguntas = [
        Pregunta(
            title="Suma dos números",
            prompt="Escribe `suma(a, b)` que devuelva a + b.",
            hints=["Usa operadores aritméticos", "Devuelve el resultado"],
            tags=["funciones", "aritmética"],
        ),
        Pregunta(
            title="Es número par",
            prompt="Escribe `es_par(n)` que devuelva `True` si n es par y `False` si es impar.",
            hints=["Usa el operador módulo %", "Compara el resultado con 0"],
            tags=["funciones", "condicionales", "booleans"],
        ),
    ]

    cargar_preguntas("problems.yaml", preguntas)
    print("Preguntas cargadas desde POO antes de continuar.")


if __name__ == "__main__":
    main()