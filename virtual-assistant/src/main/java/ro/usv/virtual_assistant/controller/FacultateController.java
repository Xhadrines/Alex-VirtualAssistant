// Definește unde se află clasa în proiect.
package ro.usv.virtual_assistant.controller;

// Importurile necesare pentru Spring MVC (Model-View-Controller).
import org.springframework.stereotype.Controller; // Anotare pentru a marca clasa ca un controller Spring.
import org.springframework.ui.Model; // Clasă folosită pentru a adăuga atribute modelului.
import org.springframework.web.bind.annotation.GetMapping; // Anotare pentru a gestiona cererile GET.
import org.springframework.web.client.RestTemplate; // Clasă pentru a efectua cereri REST.

/**
 * Controller pentru gestionarea cererilor legate de facultate.
 * Această clasă returnează conținutul de pe pagina FIESC.
 *
 * @author Șandru Alexandru
 * @version 0.1.1
 * @since 26-10-2024
 */
@Controller // Indică faptul că această clasă este un controller MVC.
public class FacultateController {

    /**
     * Endpoint pentru cererile de tip GET la URL-ul specificat.
     * 
     * @param model Modelul utilizat pentru a adăuga atribute ce vor fi accesate în fișierul HTML.
     * @return Numele fișierului HTML ce va fi utilizat pentru a răspunde cererii.
     */
    @GetMapping("/fiesc") // URL-ul endpoint-ului pentru cererea GET.
    public String getFacultatePage(Model model) {
        RestTemplate restTemplate = new RestTemplate(); // Crează o instanță a RestTemplate pentru a efectua cereri HTTP.
        String url = "https://fiesc.usv.ro/"; // URL-ul de la care se va obține conținutul paginii.

        // Obține conținutul paginii de la URL-ul specificat.
        String response = restTemplate.getForObject(url, String.class);
        
        // Adaugă răspunsul la model, astfel încât să poată fi accesat în fișierul HTML.
        model.addAttribute("content", response);
        
        return "facultate"; // Returnează numele fișierului HTML care va fi utilizat pentru a răspunde.
    }
}
