package com.mtech.orders.controller;

import com.mtech.orders.dto.CreateOrderRequest;
import com.mtech.orders.dto.OrderResponse;
import com.mtech.orders.exception.GlobalExceptionHandler;
import com.mtech.orders.exception.OrderNotFoundException;
import com.mtech.orders.service.OrderService;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.WebMvcTest;
import org.springframework.context.annotation.Import;
import org.springframework.http.MediaType;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.context.bean.override.mockito.MockitoBean;

import java.time.Instant;
import java.util.List;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.when;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;

@WebMvcTest(OrderController.class)
@Import(GlobalExceptionHandler.class)
class OrderControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockitoBean
    private OrderService orderService;

    @Test
    void createsOrder() throws Exception {
        when(orderService.createOrder(any(CreateOrderRequest.class)))
                .thenReturn(orderResponse(1L, "Ava", "Keyboard", 2));

        mockMvc.perform(post("/api/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"customerName":"Ava","productName":"Keyboard","quantity":2}
                                """))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.customerName").value("Ava"))
                .andExpect(jsonPath("$.productName").value("Keyboard"))
                .andExpect(jsonPath("$.quantity").value(2));

        verify(orderService).createOrder(new CreateOrderRequest("Ava", "Keyboard", 2));
    }

    @Test
    void rejectsInvalidOrder() throws Exception {
        mockMvc.perform(post("/api/orders")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"customerName":" ","productName":"","quantity":0}
                                """))
                .andExpect(status().isBadRequest())
                .andExpect(jsonPath("$.validationErrors.customerName").exists())
                .andExpect(jsonPath("$.validationErrors.productName").exists())
                .andExpect(jsonPath("$.validationErrors.quantity").exists());

        verifyNoInteractions(orderService);
    }

    @Test
    void returnsOrderById() throws Exception {
        when(orderService.getOrder(1L)).thenReturn(orderResponse(1L, "Ava", "Keyboard", 2));

        mockMvc.perform(get("/api/orders/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.id").value(1))
                .andExpect(jsonPath("$.customerName").value("Ava"));
    }

    @Test
    void returnsNotFoundForUnknownOrder() throws Exception {
        when(orderService.getOrder(404L)).thenThrow(new OrderNotFoundException(404L));

        mockMvc.perform(get("/api/orders/404"))
                .andExpect(status().isNotFound())
                .andExpect(jsonPath("$.status").value(404))
                .andExpect(jsonPath("$.message").value("Order with id 404 was not found"));
    }

    @Test
    void listsOrders() throws Exception {
        when(orderService.getOrders()).thenReturn(List.of(
                orderResponse(1L, "Ava", "Keyboard", 2)
        ));

        mockMvc.perform(get("/api/orders"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].id").value(1))
                .andExpect(jsonPath("$[0].productName").value("Keyboard"));
    }

    @Test
    void exposesTestEndpoint() throws Exception {
        mockMvc.perform(get("/api/test"))
                .andExpect(status().isOk())
                .andExpect(content().string("Order service is running"));
    }

    private static OrderResponse orderResponse(Long id, String customerName, String productName, int quantity) {
        return new OrderResponse(id, customerName, productName, quantity, Instant.parse("2026-01-01T12:00:00Z"));
    }
}
