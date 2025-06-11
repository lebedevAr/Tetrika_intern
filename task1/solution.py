def strict(function):
    def wrapped(*args, **kwargs):
        annotations = function.__annotations__

        for name, value in zip(annotations.keys(), args):
            if not isinstance(value, annotations[name]):
                raise TypeError(
                    f"Argument '{name}' must be {annotations[name]}, not {type(value)}"
                )

        # Обработка именнованных аргументов
        for name, value in kwargs.items():
            if name in annotations and not isinstance(value, annotations[name]):
                raise TypeError(
                    f"Argument '{name}' must be {annotations[name]}, not {type(value)}"
                )
        return function(*args, **kwargs)
    return wrapped


@strict
def sum_two(a: int, b: int) -> int:
    return a + b


if __name__ == '__main__':
    print(sum_two(1, 2))  # >>> 3
    print(sum_two(1, 2.4))  # >>> TypeError