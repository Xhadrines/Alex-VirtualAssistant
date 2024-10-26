// Definește unde se află clasa în proiect.
package ro.usv.virtual_assistant;

// Importurile necesare pentru testare.
import org.junit.jupiter.api.Test; // Importă anotarea pentru a defini metodele de testare.
// Importă anotarea pentru a configura testele Spring Boot.
import org.springframework.boot.test.context.SpringBootTest;

/**
 * Clasa de teste pentru aplicația Spring Boot.
 * Această clasă conține teste pentru a verifica dacă contextul aplicației
 * se încarcă corect.
 *
 * @author Șandru Alexandru
 * @version 0.1.1
 * @since 26-10-2024
 */
@SpringBootTest // Indică faptul că este un test care va verifica contextul Spring.
class AlexSpringApplicationBuilderTests {

    /**
     * Test de încărcare a contextului aplicației.
     * Aceasta va verifica dacă aplicația se poate porni fără erori.
     */
    @Test // Anotare care marchează această metodă ca un test.
    void contextLoads() {
        // Verifică dacă contextul aplicației se încarcă corect.
    	// Testul va trece dacă nu apar erori la încărcarea contextului.
    }

}
