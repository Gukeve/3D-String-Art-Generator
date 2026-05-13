package com.example.stringart.feature.cipher.data

import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import kotlinx.serialization.encodeToString
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.json.Json

class CipherMappingStore(private val dataStore: DataStore<Preferences>) {
    private val key = stringPreferencesKey("cipher_mapping_json")

    val mappingFlow: Flow<Map<String, String>> = dataStore.data.map { prefs ->
        prefs[key]?.let { Json.decodeFromString<Map<String, String>>(it) } ?: emptyMap()
    }

    suspend fun save(mapping: Map<String, String>) {
        dataStore.edit { it[key] = Json.encodeToString(mapping) }
    }
}
