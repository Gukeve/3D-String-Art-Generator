package com.example.stringart.feature.cipher.domain

object CipherDefaults {
    const val MAX_LENGTH = 50_000

    val defaultMap: Map<String, String> = mapOf(
        "А" to "A", "Б" to "B", "В" to "C", "Г" to "D", "Д" to "E", "Е" to "F", "Ё" to "G", "Ж" to "H",
        "З" to "I", "И" to "J", "Й" to "K", "К" to "L", "Л" to "M", "М" to "N", "Н" to "O", "О" to "P",
        "П" to "Q", "Р" to "R", "С" to "S", "Т" to "T", "У" to "U", "Ф" to "V", "Х" to "W", "Ц" to "X",
        "Ч" to "Y", "Ш" to "Z", "Щ" to "^", "Ъ" to "…", "Ы" to "[", "Ю" to "<", "Я" to "{", "Ь" to "*", "Э" to "⟪",
        "а" to "a", "б" to "b", "в" to "c", "г" to "d", "д" to "e", "е" to "f", "ё" to "g", "ж" to "h",
        "з" to "i", "и" to "j", "й" to "k", "к" to "l", "л" to "m", "м" to "n", "н" to "o", "о" to "p",
        "п" to "q", "р" to "r", "с" to "s", "т" to "t", "у" to "u", "ф" to "v", "х" to "w", "ц" to "x",
        "ч" to "y", "ш" to "z", "щ" to "|", "ъ" to "‖", "ы" to "]", "ю" to ">", "я" to "}", "ь" to "#", "э" to "$"
    )
}
