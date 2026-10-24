package com.mtech.orders.service;

import com.mtech.orders.dto.CreateOrderRequest;
import com.mtech.orders.dto.OrderResponse;
import com.mtech.orders.entity.CustomerOrder;
import com.mtech.orders.exception.OrderNotFoundException;
import com.mtech.orders.repository.OrderRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.List;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
class OrderServiceTest {

    @Mock
    private OrderRepository orderRepository;

    @InjectMocks
    private OrderService orderService;

    @Test
    void createsOrderAndMapsSavedEntity() {
        CreateOrderRequest request = new CreateOrderRequest("Ava", "Keyboard", 2);
        CustomerOrder savedOrder = new CustomerOrder("Ava", "Keyboard", 2);
        when(orderRepository.save(org.mockito.ArgumentMatchers.any(CustomerOrder.class)))
                .thenReturn(savedOrder);

        OrderResponse response = orderService.createOrder(request);

        ArgumentCaptor<CustomerOrder> orderCaptor = ArgumentCaptor.forClass(CustomerOrder.class);
        verify(orderRepository).save(orderCaptor.capture());
        assertEquals("Ava", orderCaptor.getValue().getCustomerName());
        assertEquals("Keyboard", orderCaptor.getValue().getProductName());
        assertEquals(2, orderCaptor.getValue().getQuantity());
        assertEquals("Ava", response.customerName());
        assertEquals("Keyboard", response.productName());
        assertEquals(2, response.quantity());
    }

    @Test
    void returnsOrderWhenIdExists() {
        CustomerOrder order = new CustomerOrder("Ava", "Keyboard", 2);
        when(orderRepository.findById(1L)).thenReturn(Optional.of(order));

        OrderResponse response = orderService.getOrder(1L);

        assertEquals("Ava", response.customerName());
        assertEquals("Keyboard", response.productName());
        assertEquals(2, response.quantity());
    }

    @Test
    void throwsNotFoundWhenIdDoesNotExist() {
        when(orderRepository.findById(404L)).thenReturn(Optional.empty());

        OrderNotFoundException exception = assertThrows(
                OrderNotFoundException.class,
                () -> orderService.getOrder(404L)
        );

        assertEquals("Order with id 404 was not found", exception.getMessage());
    }

    @Test
    void returnsAllOrders() {
        when(orderRepository.findAll()).thenReturn(List.of(
                new CustomerOrder("Ava", "Keyboard", 2),
                new CustomerOrder("Noah", "Mouse", 1)
        ));

        List<OrderResponse> responses = orderService.getOrders();

        assertEquals(2, responses.size());
        assertEquals("Ava", responses.get(0).customerName());
        assertEquals("Noah", responses.get(1).customerName());
    }
}
