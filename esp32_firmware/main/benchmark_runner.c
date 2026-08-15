#include <stdint.h>
#include <inttypes.h>
#include "esp_timer.h"
#include "esp_log.h"

static const char *TAG = "BENCHMARK";

int64_t benchmark_start(void)
{
    return esp_timer_get_time();
}

void benchmark_end(int64_t start_time)
{
    int64_t end_time = esp_timer_get_time();
    int64_t elapsed_us = end_time - start_time;

    ESP_LOGI(
        TAG,
        "Inference time: %" PRId64 " us",
        elapsed_us
    );
}