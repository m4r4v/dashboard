/**
 * Service Layer: Items (Blueprint)
 * Abstracción de endpoints para gestión de inventario.
 */
import api from './api'

const RESOURCE = '/api/v1/items'

export default {
  /**
   * Obtener lista completa de items
   * @returns {Promise<Array>}
   */
  getAll() {
    return api.get(RESOURCE)
  },

  /**
   * Crear un nuevo item
   * @param {Object} data - Payload del item (title, description)
   * @returns {Promise<Object>} - Item creado
   */
  create(data) {
    return api.post(RESOURCE, data)
  },

  /**
   * Actualizar un item existente
   * @param {number|string} id - ID del item
   * @param {Object} data - Datos a actualizar
   */
  update(id, data) {
    return api.put(`${RESOURCE}/${id}`, data)
  },

  /**
   * Eliminar un item
   * @param {number|string} id - ID del item
   */
  delete(id) {
    return api.delete(`${RESOURCE}/${id}`)
  }
}
