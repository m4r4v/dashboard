/**
 * Items Store (Pinia)
 * Gestión de estado para el inventario.
 */
import { defineStore } from 'pinia'
import { ref } from 'vue'
import itemsService from '@/services/items'

export const useItemsStore = defineStore('items', () => {
  // --- STATE ---
  const items = ref([])
  const loading = ref(false)
  const error = ref(null)

  // --- ACTIONS ---

  /**
   * Cargar todos los items desde la API
   */
  async function fetchItems() {
    loading.value = true
    error.value = null
    try {
      const response = await itemsService.getAll()
      items.value = response.data
    } catch (error_) {
      console.error('Error fetching items:', error_)
      error.value = 'No se pudieron cargar los datos.'
    } finally {
      loading.value = false
    }
  }

  /**
   * Crear un nuevo item
   * @param {Object} payload - { title, description }
   */
  async function createItem(payload) {
    loading.value = true
    error.value = null
    try {
      const response = await itemsService.create(payload)
      // Opción A: Agregar a la lista local (Optimista/Rápido)
      items.value.push(response.data)
      return true
    } catch (error_) {
      console.error('Error creating item:', error_)
      error.value = 'Error al crear el item.'
      return false
    } finally {
      loading.value = false
    }
  }

  /**
   * Eliminar un item
   * @param {number} id
   */
  async function deleteItem(id) {
    loading.value = true
    error.value = null
    try {
      await itemsService.delete(id)
      // Eliminamos localmente para evitar recargar toda la lista
      items.value = items.value.filter(item => item.id !== id)
      return true
    } catch (error_) {
      console.error('Error deleting item:', error_)
      error.value = 'Error al eliminar el item.'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    items,
    loading,
    error,
    fetchItems,
    createItem,
    deleteItem
  }
})
