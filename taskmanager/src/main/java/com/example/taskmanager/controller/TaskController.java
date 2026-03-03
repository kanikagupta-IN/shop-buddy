package com.example.taskmanager.controller;

import com.example.taskmanager.model.Task;
import com.example.taskmanager.service.TaskService;
import io.swagger.v3.oas.annotations.Operation;
import io.swagger.v3.oas.annotations.tags.Tag;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.security.Principal;
import java.util.List;

@Slf4j
@RestController
@RequestMapping("/tasks")
@Tag(name = "task-controller", description = "This controller provides all the endpoints related to task.")
public class TaskController {
    @Autowired
    private TaskService taskService;

    @Operation(summary = "Create a task.")
    @PostMapping
    public ResponseEntity<Task> createTask(@RequestBody Task task, Principal principal) {
        log.info("Received request to create a task");
        return ResponseEntity.status(HttpStatus.CREATED).body(taskService.createTask(task, principal.getName()));
    }

    @Operation(summary = "Get the list of tasks.")
    @GetMapping
    public ResponseEntity<List<Task>> getTasks(Principal principal) {
        log.info("Received request to get list of tasks");
        return ResponseEntity.ok(taskService.getTasks(principal.getName()));
    }

    @Operation(summary = "Get a task.")
    @GetMapping("/{id}")
    public ResponseEntity<Task> getTask(@PathVariable Long id, Principal principal) {
        log.info("Received request to get a task");
        return ResponseEntity.ok(taskService.getTask(id, principal.getName()));
    }

    @Operation(summary = "Update a task.")
    @PutMapping("/{id}")
    public ResponseEntity<Task> updateTask(@PathVariable Long id, @RequestBody Task task, Principal principal) {
        log.info("Received request to update a task");
        return ResponseEntity.ok(taskService.updateTask(id, task, principal.getName()));
    }

    @Operation(summary = "Delete a task.")
    @DeleteMapping("/{id}")
    public ResponseEntity<?> deleteTask(@PathVariable Long id, Principal principal) {
        log.info("Received request to delete a task");
        taskService.deleteTask(id, principal.getName());
        return ResponseEntity.noContent().build();
    }
}
