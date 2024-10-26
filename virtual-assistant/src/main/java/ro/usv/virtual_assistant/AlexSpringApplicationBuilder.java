// Definește unde se află clasa în proiect.
package ro.usv.virtual_assistant;

// Importurile necesare pentru Spring Boot.
import org.springframework.boot.SpringApplication; // Pentru a porni aplicația Spring.
import org.springframework.boot.autoconfigure.SpringBootApplication; // Pentru a activa configurarea automată a aplicației.

/**
 * Clasa principală.
 * Aceasta pornește aplicația Spring Boot.
 *
 * @author Șandru Alexandru
 * @version 0.1.1
 * @since 26-10-2024
 */
@SpringBootApplication // Activează configurarea automată a aplicație.
public class AlexSpringApplicationBuilder {

    /**
     * Metoda principală care pornește aplicația.
     *
     * @param args Argumentele din linia de comandă.
     */
    public static void main(String[] args) {
        // Pornește aplicația Spring Boot.
        SpringApplication.run(AlexSpringApplicationBuilder.class, args);
    }
}
