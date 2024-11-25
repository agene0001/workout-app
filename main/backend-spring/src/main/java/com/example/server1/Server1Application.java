package com.example.server1;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;

@SpringBootApplication
//@ComponentScan(basePackages = "com.example.server1.recipe") // Ensure correct package scanning

public class  Server1Application {

    public static void main(String[] args) {
        SpringApplication.run(Server1Application.class, args);
    }

}
