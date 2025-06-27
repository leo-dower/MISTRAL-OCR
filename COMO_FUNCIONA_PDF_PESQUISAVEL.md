# Como Funciona o PDF Pesquisável

## 🎯 Objetivo

Criar um PDF onde você pode **selecionar, copiar e pesquisar** o texto, mantendo a **aparência visual original** do documento.

## 🔧 Como Funciona

### 1. **Texto Invisível Sobreposto**
- O PDF original permanece **exatamente igual** visualmente
- Uma camada de **texto invisível** é adicionada por cima
- Quando você clica no PDF, seleciona o texto invisível correspondente
- O texto invisível está **perfeitamente alinhado** com o texto da imagem

### 2. **Processo Técnico**

```
PDF Original (imagem) → OCR → Texto extraído → PDF + Texto Invisível
     ↓                    ↓         ↓              ↓
   Mantido           Tesseract   "Olá mundo"    PDF Pesquisável
   intacto           ou Mistral    extraído      (selecionável)
```

### 3. **Três Métodos Disponíveis**

#### 🔄 **Método Overlay (Padrão)**
- **Mais compatível**
- Adiciona texto invisível por cima da imagem
- Funciona em qualquer visualizador de PDF
- **Recomendado** para a maioria dos casos

#### 📄 **Método Layer** 
- Cria uma nova camada de texto
- Mais avançado, melhor separação
- Ainda em desenvolvimento

#### 🔄 **Método Replace**
- Substitui completamente o conteúdo
- Para casos específicos
- Ainda em desenvolvimento

## ⚙️ Configurações Disponíveis

### **Controle de Qualidade**
- **Confiança Mínima**: 0.1 a 1.0
- Só adiciona texto se a confiança OCR for alta o suficiente
- Evita texto com muitos erros no PDF final

### **Opções de Saída**
- ✅ **JSON**: Dados completos do OCR
- ✅ **Markdown**: Texto limpo e formatado  
- ✅ **PDF Pesquisável**: PDF original + texto selecionável
- ⚙️ **Manter Original**: PDF original não é modificado

## 🚀 Vantagens

### **Para o Usuário**
- 📄 **Selecionar texto** diretamente no PDF
- 🔍 **Pesquisar** palavras no PDF
- 📋 **Copiar** texto para outros aplicativos
- 📧 **Enviar** PDFs que outros podem pesquisar

### **Para Advocacia/Escritórios**
- 📚 **Arquivo digital pesquisável** de processos
- 🔍 **Buscar** rapidamente em centenas de documentos
- 📝 **Citar** trechos específicos facilmente
- 🗂️ **Organizar** biblioteca digital

### **Compatibilidade**
- ✅ **Adobe Reader**
- ✅ **Google Chrome**
- ✅ **Firefox**
- ✅ **Edge**
- ✅ **Visualizadores móveis**

## 🔍 Como Usar

### **1. Selecionar Formatos de Saída**
```
☑️ Gerar JSON
☑️ Gerar Markdown  
☑️ Gerar PDF pesquisável ← NOVA FUNCIONALIDADE
```

### **2. Configurar PDF**
```
☑️ Manter PDF original
Confiança mín: [====•===] 0.7
Método: ⚫ Sobreposição invisível
```

### **3. Processar**
- Arquivo original: `contrato.pdf`
- **Resultado**: `contrato_pesquisavel.pdf`

### **4. Testar**
1. Abra `contrato_pesquisavel.pdf`
2. Tente selecionar texto com o mouse
3. Use Ctrl+F para pesquisar
4. Copy/paste funcionará!

## 📊 Exemplo Prático

### **Antes (PDF Escaneado)**
```
[Imagem do documento]
❌ Não é possível selecionar texto
❌ Ctrl+F não encontra nada
❌ Ctrl+C não funciona
```

### **Depois (PDF Pesquisável)**
```
[Mesma imagem do documento]
✅ Texto selecionável com mouse
✅ Ctrl+F encontra qualquer palavra
✅ Ctrl+C copia texto corretamente
✅ Visualmente idêntico ao original
```

## 🔧 Dependências Técnicas

### **Bibliotecas Usadas**
- **PyMuPDF**: Manipulação avançada de PDF
- **ReportLab**: Geração de elementos PDF
- **OCR Engine**: Tesseract (local) ou Mistral AI (cloud)

### **Instalação**
```bash
pip install PyMuPDF reportlab
sudo apt install tesseract-ocr  # Para OCR local
```

## ⚠️ Limitações

### **Qualidade do OCR**
- Depende da qualidade da imagem original
- Texto com baixa confiança pode ser ignorado
- Documentos muito antigos podem ter problemas

### **Alinhamento**
- Texto invisível pode não estar perfeitamente alinhado
- Funciona melhor com documentos de texto simples
- Tabelas complexas podem ter alinhamento imperfeito

### **Tamanho do Arquivo**
- PDF pesquisável é um pouco maior que o original
- Diferença típica: +10% a +30% do tamanho original

## 🎯 Casos de Uso Ideais

### **✅ Perfeito Para:**
- Contratos escaneados
- Documentos jurídicos
- Relatórios em PDF
- Livros digitalizados
- Faturas e notas fiscais

### **⚠️ Cuidado Com:**
- Documentos com muitas imagens
- PDFs já pesquisáveis (redundante)
- Documentos com layout muito complexo
- Texto em ângulos ou rotacionado

## 📈 Estatísticas Mostradas

A aplicação mostra em tempo real:
- **PDFs criados**: Quantos foram gerados
- **Tamanho total**: Espaço usado pelos PDFs
- **Taxa de sucesso**: % de páginas com texto adicionado
- **Tempo de processamento**: Por arquivo e total

## 🔄 Fluxo Completo

1. **Selecionar PDFs** → Lista de arquivos
2. **Configurar OCR** → Local/Cloud/Híbrido  
3. **Configurar Saída** → JSON + MD + PDF pesquisável
4. **Processar** → OCR + Geração de formatos
5. **Resultado** → 3 arquivos por PDF original:
   - `documento_OCR_completo.json`
   - `documento_OCR.md`
   - `documento_pesquisavel.pdf` ← **NOVO!**

Esta funcionalidade transforma seus PDFs "mortos" em documentos **vivos e pesquisáveis**! 🎉