package com.mtech.orders.service;

import com.mtech.orders.dto.CreateOrderRequest;
import com.mtech.orders.dto.OrderResponse;
import com.mtech.orders.entity.CustomerOrder;
import com.mtech.orders.exception.OrderNotFoundException;
import com.mtech.orders.repository.OrderRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class OrderService {

    private final OrderRepository orderRepository;

    public OrderService(OrderRepository orderRepository) {
        this.orderRepository = orderRepository;
    }

    public OrderResponse createOrder(CreateOrderRequest request) {
        CustomerOrder order = new CustomerOrder(
                request.customerName(),
                request.productName(),
                request.quantity()
        );
        return toResponse(orderRepository.save(order));
    }

    public OrderResponse getOrder(Long id) {
        CustomerOrder order = orderRepository.findById(id)
                .orElseThrow(() -> new OrderNotFoundException(id));
        return toResponse(order);
    }

    public List<OrderResponse> getOrders() {
        return orderRepository.findAll().stream()
                .map(OrderService::toResponse)
                .toList();
    }

    private static OrderResponse toResponse(CustomerOrder order) {
        return new OrderResponse(
                order.getId(),
                order.getCustomerName(),
                order.getProductName(),
                order.getQuantity(),
                order.getCreatedAt()
        );
    }
}
