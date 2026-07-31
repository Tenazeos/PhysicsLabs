superscript_digits = str.maketrans("0123456789+-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻")


def scientific_superscript(value: float, precision: int = 1) -> str:
    base, exponent = f"{value:.{precision}e}".split("e")
    exp_superscript = str(int(exponent)).translate(superscript_digits)

    return f"{base}×10{exp_superscript}"  # noqa: RUF001
