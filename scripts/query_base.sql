create table clientes (
  id bigint primary key generated always as identity,
  nombre text not null,
  email text unique not null
);

create table frecuencia_pagos (
  id bigint primary key generated always as identity,
  frequencia text not null check (
    frequencia in (
      'Semanal',
      'Mensual',
      'Trimestral',
      'Semestral',
      'Anual'
    )
  )
);

create table pagos (
  id bigint primary key generated always as identity,
  cliente_id bigint references clientes (id),
  cantidad numeric(10, 2) not null,
  fecha_inicio date not null,
  fecha_fin date not null,
  frecuencia_pagos_id bigint references frecuencia_pagos (id),
  fechas_pagos date[0],
  completado boolean not null default false
);

-- Tabla para registrar cada fecha de pago de un cliente
create table fechas_pago (
  id bigint primary key generated always as identity,
  pago_id bigint references pagos(id) on delete cascade,
  fecha date not null,
  pagado boolean not null default false
);
