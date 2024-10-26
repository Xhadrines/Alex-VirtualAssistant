// Definește unde se află clasa în proiect.
package ro.usv.virtual_assistant.config;

// Importurile necesare pentru configurarea aplicației.
import org.springframework.boot.builder.SpringApplicationBuilder; // Pentru construirea aplicației Spring.
import org.springframework.boot.web.servlet.support.SpringBootServletInitializer; // Suport pentru inițializarea servlet-ului.

// Importul clasei principale a aplicației.
import ro.usv.virtual_assistant.AlexSpringApplicationBuilder;

/**
 * Clasa de inițializare a servlet-ului pentru aplicația Spring Boot.
 * Aceasta extinde funcționalitatea SpringBootServletInitializer pentru a permite
 * aplicației să fie implementată pe un server de aplicații.
 *
 * @author Șandru Alexandru
 * @version 0.1.1
 * @since 26-10-2024
 */
public class ServletInitializer extends SpringBootServletInitializer {

    /**
     * Configurează aplicația pentru a fi utilizată cu un server de aplicații.
     *
     * @param application Builder-ul aplicației.
     * @return Builder-ul configurat cu sursa aplicației principale.
     */
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        // Specifică clasa principală a aplicației.
        return application.sources(AlexSpringApplicationBuilder.class);
    }

}
