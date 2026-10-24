package com.mtech.orders.dto;

import java.time.Instant;

public record OrderResponse(
        Long id,
        String customerName,
        String productName,
        int quantity,
        Instant createdAt
) {
}
