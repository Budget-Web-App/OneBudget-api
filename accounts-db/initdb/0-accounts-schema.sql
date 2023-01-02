CREATE TABLE IF NOT EXISTS users (
  userid CHAR(10) PRIMARY KEY,
  email VARCHAR(64) UNIQUE NOT NULL,
  passhash BYTEA NOT NULL,
  registereddate DATE,
  timezone VARCHAR(9) NOT NULL
);

CREATE TABLE IF NOT EXISTS budgets (
  budgetid CHAR(10) PRIMARY KEY,
  displayname VARCHAR(255) NOT NULL,
  budgetnotes VARCHAR(255),
  accessdate DATE NOT NULL,
  userid CHAR(10) NOT NULL,
  CONSTRAINT fk_userid Foreign key (userid) references users (userid)
);

CREATE TABLE IF NOT EXISTS categories (
  categoryid CHAR(10) PRIMARY KEY,
  displayname VARCHAR(255) NOT NULL,
  parentid VARCHAR(255),
  budgetid CHAR(10) NOT NULL,
  CONSTRAINT fk_budgetid Foreign key (budgetid) references budgets (budgetid)
);

CREATE INDEX IF NOT EXISTS idx_users_userid ON users (userid);
CREATE INDEX IF NOT EXISTS idx_users_email ON users (email);

CREATE INDEX IF NOT EXISTS idx_budgets_budgetid ON budgets (budgetid);

CREATE INDEX IF NOT EXISTS idx_categories_categoryid ON categories (categoryid);