package com.example.taskmanager.service;

import com.example.taskmanager.model.Task;
import com.example.taskmanager.model.User;
import com.example.taskmanager.repository.TaskRepository;
import com.example.taskmanager.repository.UserRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
public class TaskService {
    private final TaskRepository taskRepository;
    private final UserRepository userRepository;

    /**
     * Create a task
     * @param task
     * @param email
     * @return
     */
    public Task createTask(Task task, String email) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));
        task.setUser(user);
        return taskRepository.save(task);
    }

    /**
     * Get list of tasks.
     * @param email
     * @return
     */
    public List<Task> getTasks(String email) {
        User user = userRepository.findByEmail(email)
                .orElseThrow(() -> new RuntimeException("User not found"));
        return taskRepository.findByUser(user);
    }

    /**
     * Get a task.
     * @param id
     * @param email
     * @return
     */
    public Task getTask(Long id, String email) {
        Task task = taskRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Task not found"));
        if (!task.getUser().getEmail().equals(email)) {
            throw new RuntimeException("Unauthorized access");
        }
        return task;
    }

    /**
     * Update a task.
     * @param id
     * @param updatedTask
     * @param email
     * @return
     */
    public Task updateTask(Long id, Task updatedTask, String email) {
        Task task = getTask(id, email);
        task.setTitle(updatedTask.getTitle());
        task.setDescription(updatedTask.getDescription());
        task.setDueDate(updatedTask.getDueDate());
        task.setStatus(updatedTask.getStatus());
        return taskRepository.save(task);
    }

    /**
     * Delete a task.
     * @param id
     * @param email
     */
    public void deleteTask(Long id, String email) {
        Task task = getTask(id, email);
        taskRepository.delete(task);
    }
}