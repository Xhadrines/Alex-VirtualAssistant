import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './SettingsPage.css';

const API_URL = import.meta.env.VITE_CHAT_API;

const SettingsPage = () => {
    const [twoFactorAuth, setTwoFactorAuth] = useState(false);
    const navigate = useNavigate();

    const [formData, setFormData] = useState({
        nume: '',
        prenume: '',
        facultate: '',
        specializare: '',
        grupa: '',
        parolaCurenta: '',
        parolaNoua: '',
        confirmaParola: '',
    });

    useEffect(() => {
        const firstName = localStorage.getItem('first_name');
        const lastName = localStorage.getItem('last_name');
        const username = localStorage.getItem('username');

        if (firstName && lastName && username) {
            setFormData((prev) => ({
                ...prev,
                nume: firstName,
                prenume: lastName,
                facultate: '',
                specializare: '',
                grupa: '',
            }));
        }
    }, []);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData((prev) => ({...prev, [name]: value, }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
    
        if (formData.parolaNoua !== formData.confirmaParola) {
            alert('Parola noua si confirmarea nu coincid!');
            return;
        }
    
        try {
            const token = localStorage.getItem('token');
            console.log("Token extras:", token);
            
            if (!token) {
                alert('Eroare: Nu sunteti autentificat!');
                return;
            }
            
            const response = await fetch(`${API_URL}/api/user/settings/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Token ${token}`,
                },
                body: JSON.stringify({
                    nume: formData.nume,
                    prenume: formData.prenume,
                    facultate: formData.facultate,
                    specializare: formData.specializare,
                    grupa: formData.grupa,
                    parolaCurenta: formData.parolaCurenta,
                    parolaNoua: formData.parolaNoua,
                    confirmaParola: formData.confirmaParola,
                    twoFA: twoFactorAuth,
                }),
            });
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Eroare necunoscuta.');
            }
            
            alert('Setarile au fost salvate cu succes!');
        } catch (error) {
            console.error('Eroare la salvare:', error);
            alert(`A aparut o eroare: ${error.message}`);
        }
    };

    return (
        <div className="settings-container">
            <div className="header">
                <button className="back-btn" onClick={() => window.history.back()}>
                    <img src="/back.png" alt="Inapoi" className="button-icon" />
                </button>
                <h1>Setari cont</h1>
            </div>
            <form className="settings-form" onSubmit={handleSubmit}>
                <div className="input-group">
                    <label>Nume</label>
                    <input
                        type="text"
                        name="nume"
                        value={formData.nume}
                        onChange={handleChange}
                        placeholder="Introdu numele"
                    />
                </div>
                <div className="input-group">
                    <label>Prenume</label>
                    <input
                        type="text"
                        name="prenume"
                        value={formData.prenume}
                        onChange={handleChange}
                        placeholder="Introdu prenumele"
                    />
                </div>
                <div className="input-group">
                    <label>Facultatea</label>
                    <select name="facultate" value={formData.facultate} onChange={handleChange}>
                        <option value="">Selecteaza facultatea</option>
                        <option value="FIESC">FIESC</option>
                    </select>
                </div>
                <div className="input-group">
                    <label>Specializarea</label>
                    <select name="specializare" value={formData.specializare} onChange={handleChange}>
                        <option value="">Selecteaza specializarea</option>
                        <option value="Calculatoare">Calculatoare</option>
                    </select>
                </div>
                <div className="input-group">
                    <label>Grupa</label>
                    <select name="grupa" value={formData.grupa} onChange={handleChange}>
                        <option value="">Selecteaza grupa</option>
                        <option value="3142A">3142A</option>
                        <option value="3142B">3142B</option>
                    </select>
                </div>
                <div className="input-group">
                    <label>Parola curenta</label>
                    <input
                        type="password"
                        name="parolaCurenta"
                        value={formData.parolaCurenta}
                        onChange={handleChange}
                        placeholder="Parola actuala"
                    />
                </div>
                <div className="input-group">
                    <label>Parola noua</label>
                    <input
                        type="password"
                        name="parolaNoua"
                        value={formData.parolaNoua}
                        onChange={handleChange}
                        placeholder="Noua parola"
                    />
                </div>
                <div className="input-group">
                    <label>Confirma parola noua</label>
                    <input
                        type="password"
                        name="confirmaParola"
                        value={formData.confirmaParola}
                        onChange={handleChange}
                        placeholder="Confirmare parola"
                    />
                </div>
                <div className="input-group switch-group">
                    <label>Autentificare in 2 factori</label>
                    <label className="switch">
                        <input
                            type="checkbox"
                            checked={twoFactorAuth}
                            onChange={() => setTwoFactorAuth(!twoFactorAuth)}
                        />
                        <span className="slider"></span>
                    </label>
                </div>
                <button className="settings-btn" type="submit">
                    Aplica setarile
                </button>
            </form>
        </div>
    );
};

export default SettingsPage;
