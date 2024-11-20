# Project: Django Formset Study

Este repositório contém um **projeto acadêmico** desenvolvido com o propósito de estudar e compreender o funcionamento dos **formsets no Django**. Ele serve como um exemplo prático para aqueles que desejam aprimorar seus conhecimentos em **formulários dinâmicos** e manipulação de múltiplos registros em uma única página.

## 💡 **Sobre o Projeto**

O objetivo principal deste projeto é explorar o uso de **formsets** no Django para lidar com múltiplos formulários de maneira eficiente. Ele aborda aspectos fundamentais e boas práticas para trabalhar com:

- Formsets padrão e inline formsets.
- Validações personalizadas nos formsets.
- Manipulação de dados de formulários relacionados em uma única requisição.
- Renderização dinâmica de formulários no template.

Este projeto é uma **base de aprendizado**, ideal para desenvolvedores que estão aprofundando suas habilidades em **Django Forms**.

## 🚀 **Principais Funcionalidades**

- Adição, edição e remoção de múltiplos registros em uma única página.
- Formsets dinâmicos, permitindo a inclusão de novos formulários sem recarregar a página.
- Integração com o Django Admin para gerenciar os dados.
- Suporte para validações personalizadas e controle de erros.

## 🛠️ **Tecnologias Utilizadas**

- [Python](https://www.python.org/) 3.9+
- [Django](https://www.djangoproject.com/) 4.x
- Banco de dados SQLite (padrão para estudos)

## 🗂️ **Estrutura do Projeto**

```plaintext
project/
│
├── app/                   # App principal do projeto
│   ├── forms.py           # Formsets e formulários personalizados
│   ├── models.py          # Modelos do banco de dados
│   ├── views.py           # Lógica para manipulação de formsets
│   ├── templates/         # Templates HTML para os formsets
│       └── formset.html   # Página principal de exemplo com formsets
│   └── static/            # Arquivos estáticos (CSS/JS)
│
├── manage.py              # Comando principal do Django
├── db.sqlite3             # Banco de dados SQLite
└── settings.py            # Configurações do projeto
```

## ⚙️ **Configuração e Execução**

1. Clone o repositório:
   ```bash
   git clone https://github.com/carlosalbertoprojetos/project.git
   cd project
   ```

2. Crie um ambiente virtual e instale as dependências:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Realize as migrações do banco de dados:
   ```bash
   python manage.py migrate
   ```

4. Crie um superusuário para acessar o admin:
   ```bash
   python manage.py createsuperuser
   ```

5. Inicie o servidor de desenvolvimento:
   ```bash
   python manage.py runserver
   ```

6. Acesse o projeto em seu navegador:
   - Página de formsets: [http://127.0.0.1:8000/formset/](http://127.0.0.1:8000/formset/)
   - Django Admin: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## 📚 **Propósito Educacional**

Este projeto é exclusivamente para **fins educacionais** e não é indicado para produção. Ele fornece uma introdução prática ao uso de formsets no Django, permitindo uma compreensão detalhada de seus conceitos.

## 🌟 **Próximos Passos**

- Adicionar validações em nível de formset para cenários específicos.
- Explorar a integração com JavaScript para formsets dinâmicos no frontend.
- Implementar testes automatizados para garantir a consistência do comportamento.

## 📄 **Licença**

Este projeto está sob a [Licença MIT](LICENSE). Sinta-se à vontade para utilizá-lo, adaptá-lo e melhorá-lo para seus próprios estudos e projetos.

---

💻 Desenvolvido por [Carlos Alberto Medeiros](https://www.linkedin.com/in/carlos-alberto-medeiros-29aa6258/)  
🌟 Contribua para o aprendizado de **Django Formsets**!
