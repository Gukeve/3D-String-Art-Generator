package com.example.stringart.feature.cipher.domain

class CipherEngine {
    fun encrypt(text: String, mapping: Map<String, String>): String = buildString(text.length) {
        text.forEach { ch -> append(mapping[ch.toString()] ?: ch) }
    }

    fun decrypt(text: String, mapping: Map<String, String>): String {
        val reverse = mapping.entries.associate { it.value to it.key }
        return buildString(text.length) {
            text.forEach { ch -> append(reverse[ch.toString()] ?: ch) }
        }
    }
}
