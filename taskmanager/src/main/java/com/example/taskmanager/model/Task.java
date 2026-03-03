package com.example.taskmanager.model;

import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import lombok.Data;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;
//import org.springframework.data.annotation.Id;

import java.time.LocalDate;
//import java.util.UUID;

@Entity
@Data
public class Task {
    @Id
    @GeneratedValue
    @JdbcTypeCode(SqlTypes.CHAR)
    private Long id;
    private String title;
    private String description;
    private LocalDate dueDate;
    private Status status;
    @ManyToOne
    private User user;

    public enum Status {
        PENDING, COMPLETED
    }
}
