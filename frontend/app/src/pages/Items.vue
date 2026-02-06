<template>
  <v-container class="pa-6" fluid>
    <v-row>
      <v-col cols="12">
        <v-card class="elevation-2">

          <v-toolbar color="white" flat>
            <v-toolbar-title class="text-h6 font-weight-bold">
              Inventario de Items
            </v-toolbar-title>
            <v-divider class="mx-4" inset vertical />
            <v-spacer />

            <v-btn
              color="primary"
              prepend-icon="mdi-plus"
              variant="elevated"
              @click="dialog = true"
            >
              Nuevo Item
            </v-btn>
          </v-toolbar>

          <v-data-table
            :headers="headers"
            hover
            :items="store.items"
            :loading="store.loading"
          >
            <template #loading>
              <v-skeleton-loader type="table-row@5" />
            </template>

            <template #item.actions="{ item }">
              <v-btn
                color="error"
                icon="mdi-delete"
                size="small"
                variant="text"
                @click="confirmDelete(item)"
              />
            </template>

            <template #no-data>
              <v-alert
                class="mt-4"
                icon="mdi-package-variant-closed"
                type="info"
                variant="tonal"
              >
                No hay items registrados. ¡Crea el primero!
              </v-alert>
            </template>
          </v-data-table>

        </v-card>
      </v-col>
    </v-row>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="text-h5">Nuevo Item</span>
        </v-card-title>

        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.name"
                  autofocus
                  density="compact"
                  label="Nombre"
                  variant="outlined"
                />
              </v-col>
              <v-col cols="12">
                <v-text-field
                  v-model="editedItem.description"
                  density="compact"
                  label="Descripción"
                  variant="outlined"
                />
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>

        <v-card-actions>
          <v-spacer />
          <v-btn color="blue-darken-1" variant="text" @click="close">
            Cancelar
          </v-btn>
          <v-btn color="blue-darken-1" variant="text" @click="save">
            Guardar
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialogDelete" max-width="500px">
      <v-card>
        <v-card-title class="text-h5">¿Estás seguro?</v-card-title>
        <v-card-text>
          Esta acción eliminará el item permanentemente.
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn color="blue-darken-1" variant="text" @click="closeDelete">Cancelar</v-btn>
          <v-btn color="error" variant="text" @click="deleteItemConfirm">Eliminar</v-btn>
          <v-spacer />
        </v-card-actions>
      </v-card>
    </v-dialog>

  </v-container>
</template>

<script setup lang="ts">
  import { onMounted, reactive, ref } from 'vue'
  import { useItemsStore } from '@/stores/items'

  // --- Store Injection ---
  const store = useItemsStore()

  // --- Local State ---
  const dialog = ref(false)
  const dialogDelete = ref(false)
  const itemToDelete = ref<number | null>(null)

  // CORRECCIÓN: 'key: name' para coincidir con la respuesta del Backend
  // 'any' mantiene a raya a TypeScript
  const headers: any = [
    { title: 'ID', key: 'id', align: 'start' },
    { title: 'Nombre', key: 'name' },
    { title: 'Descripción', key: 'description' },
    { title: 'Acciones', key: 'actions', sortable: false, align: 'end' },
  ]

  // CORRECCIÓN: Modelo de datos alineado (name en vez de title)
  const defaultItem = { name: '', description: '' }
  const editedItem = reactive({ ...defaultItem })

  // --- Lifecycle ---
  onMounted(() => {
    store.fetchItems()
  })

  // --- Methods ---

  function close() {
    dialog.value = false
    Object.assign(editedItem, defaultItem)
  }

  async function save() {
    // CORRECCIÓN: Validación contra 'name'
    if (editedItem.name) {
      // Limpieza de Proxies para envío limpio
      const payload = { ...editedItem }

      const success = await store.createItem(payload)
      if (success) {
        close()
      }
    }
  }

  function confirmDelete(item: any) {
    itemToDelete.value = item.id
    dialogDelete.value = true
  }

  function closeDelete() {
    dialogDelete.value = false
    itemToDelete.value = null
  }

  async function deleteItemConfirm() {
    if (itemToDelete.value) {
      await store.deleteItem(itemToDelete.value)
      closeDelete()
    }
  }
</script>

<route lang="yaml">
meta:
  layout: default
  requiresAuth: true
</route>
