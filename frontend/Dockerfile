# Usar Node.js 20 Alpine
FROM node:20-alpine

# Definir diretório de trabalho
WORKDIR /app

# Expor porta do Vite (dev)
EXPOSE 3000

# Variáveis de ambiente
ENV NODE_ENV=development

# Copiar package.json e package-lock.json primeiro (para cache)
COPY package*.json ./

# Instalar dependências
RUN npm ci

# Copiar código da aplicação
COPY . .

# Comando para iniciar em modo desenvolvimento com hot reload
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]