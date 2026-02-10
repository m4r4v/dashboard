<template>
  <v-container class="pa-6" fluid>
    <div class="d-flex align-center justify-space-between mb-6">
      <div>
        <h1 class="text-h4 font-weight-bold text-primary">Welcome, Root</h1>
        <div class="text-subtitle-1 text-medium-emphasis">System status summary</div>
      </div>
      <v-btn color="primary" prepend-icon="mdi-refresh" variant="flat">Refresh</v-btn>
    </div>

    <v-row>
      <v-col cols="12" md="3" sm="6">
        <v-card class="rounded-lg" elevation="2">
          <v-card-text class="d-flex align-center">
            <v-avatar class="mr-4" color="success" size="48" variant="tonal">
              <v-icon icon="mdi-server-network" size="24" />
            </v-avatar>
            <div>
              <div class="text-caption text-medium-emphasis text-uppercase font-weight-bold">Server Status</div>
              <div class="text-h6 font-weight-bold">Online</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="rounded-lg" elevation="2">
          <v-card-text class="d-flex align-center">
            <v-avatar class="mr-4" color="primary" size="48" variant="tonal">
              <v-icon icon="mdi-account-group" size="24" />
            </v-avatar>
            <div>
              <div class="text-caption text-medium-emphasis text-uppercase font-weight-bold">Active Users</div>
              <div class="text-h6 font-weight-bold">1 (Root)</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="rounded-lg" elevation="2">
          <v-card-text class="d-flex align-center">
            <v-avatar class="mr-4" color="warning" size="48" variant="tonal">
              <v-icon icon="mdi-shield-check" size="24" />
            </v-avatar>
            <div>
              <div class="text-caption text-medium-emphasis text-uppercase font-weight-bold">Security Level</div>
              <div class="text-h6 font-weight-bold">Argon2id</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="3" sm="6">
        <v-card class="rounded-lg" elevation="2">
          <v-card-text class="d-flex align-center">
            <v-avatar class="mr-4" color="info" size="48" variant="tonal">
              <v-icon icon="mdi-tag-text" size="24" />
            </v-avatar>
            <div>
              <div class="text-caption text-medium-emphasis text-uppercase font-weight-bold">Core Version</div>
              <div class="text-h6 font-weight-bold">v1.2.0</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-4">
      <v-col cols="12">
        <v-card class="rounded-lg" elevation="2" subtitle="Latest system events" title="Recent Activity">
          <v-card-text class="h-100 d-flex align-center justify-center pa-10 text-medium-emphasis">
            <div class="text-center">
              <v-icon class="mb-2 opacity-50" icon="mdi-chart-timeline-variant" size="64" />
              <div>Waiting for telemetry data...</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

  </v-container>
</template>

<route lang="yaml">
meta:
  layout: default
</route>
