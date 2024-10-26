// Definește unde se află clasa în proiect.
package ro.usv.virtual_assistant.controller;

// Importurile necesare pentru Spring MVC (Model-View-Controller).
import org.springframework.web.bind.annotation.GetMapping; // Pentru a defini metodele de tip GET.
// Importul pentru a indica că această clasă este un controller REST.
import org.springframework.web.bind.annotation.RestController;

/**
 * Controller pentru gestionarea cererilor HTTP.
 * Această clasă definește un endpoint care returnează un mesaj de salut.
 *
 * @author Șandru Alexandru
 * @version 0.1.0
 * @since 26-10-2024
 */
@RestController // Indică faptul că această clasă este un controller REST.
public class HelloController {

    /**
     * Endpoint pentru cererile de tip GET la rădăcina aplicației.
     * 
     * @return Un mesaj de salut.
     */
    @GetMapping("/") // Maparea cererii GET către acest endpoint.
    public String sayHello() {
        return "Hello, Spring Boot!";
    }

}
