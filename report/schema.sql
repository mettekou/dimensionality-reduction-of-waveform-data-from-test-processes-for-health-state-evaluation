CREATE TABLE part (part_number TEXT PRIMARY KEY);

CREATE TABLE revision (
    part_number TEXT REFERENCES part (part_number),
    revision_number TEXT,
    PRIMARY KEY (part_number, revision_number)
);

CREATE TABLE process (
    process_version TIMESTAMP WITH TIME ZONE,
    part_number TEXT,
    revision_number TEXT,
    process_name TEXT,
    process_definition jsonb,
    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version
    ),
    FOREIGN KEY (part_number, revision_number) REFERENCES revision (part_number, revision_number)
);

CREATE TABLE variable (
    process_version TIMESTAMP WITH TIME ZONE,
    part_number TEXT,
    revision_number TEXT,
    process_name TEXT,
    variable_path TEXT [],
    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version
    ) REFERENCES process (
        part_number,
        revision_number,
        process_name,
        process_version
    )
);

CREATE TABLE quantity_variable (
    process_version TIMESTAMP WITH TIME ZONE,
    part_number TEXT,
    revision_number TEXT,
    process_name TEXT,
    variable_path TEXT [],
    quantity_variable_unit TEXT NOT NULL,
    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ) INCLUDE (
        quantity_variable_unit
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ) REFERENCES variable (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    )
);

CREATE TABLE waveform_variable (
    waveform_variable_period interval NOT NULL,
    process_version TIMESTAMP WITH TIME ZONE,
    part_number TEXT,
    revision_number TEXT,
    process_name TEXT,
    variable_path TEXT [],
    waveform_variable_unit TEXT NOT NULL,
    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ) INCLUDE (waveform_variable_period, waveform_variable_unit),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ) REFERENCES variable (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    )
);

CREATE TABLE failure_mode (
    process_version TIMESTAMP WITH TIME ZONE,
    part_number TEXT,
    revision_number TEXT,
    process_name TEXT,
    failure_mode_name TEXT,
    failure_mode_detection jsonb,

    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        failure_mode_name
    ) INCLUDE (failure_mode_detection),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version
    ) REFERENCES process (
        part_number,
        revision_number,
        process_name,
        process_version
    )
);

CREATE TABLE item (
    part_number TEXT,
    revision_number TEXT,
    item_batch_number TEXT,
    item_serial_number TEXT,
    PRIMARY KEY (
        part_number,
        revision_number,
        item_batch_number,
        item_serial_number
    ),
    FOREIGN KEY (part_number, revision_number) REFERENCES revision (part_number, revision_number)
);

CREATE TABLE execution (
    process_version TIMESTAMP WITH TIME ZONE,
    execution_start TIMESTAMP WITH TIME ZONE,
    execution_duration INTERVAL NOT NULL,
    part_number TEXT,
    revision_number TEXT,
    item_batch_number TEXT,
    item_serial_number TEXT,
    process_name TEXT,
    equipment_name TEXT,
    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        item_batch_number,
        item_serial_number
    ) REFERENCES item (
        part_number,
        revision_number,
        item_batch_number,
        item_serial_number
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version
    ) REFERENCES process (
        part_number,
        revision_number,
        process_name,
        process_version
    ),
    FOREIGN KEY (equipment_name) REFERENCES equipment (equipment_name)
);

CREATE TABLE quantity_value (
    process_version TIMESTAMP WITH TIME ZONE,
    execution_start TIMESTAMP WITH TIME ZONE,
    part_number TEXT,
    revision_number TEXT,
    process_name TEXT,
    variable_path TEXT [],
    item_batch_number TEXT,
    item_serial_number TEXT,
    equipment_name TEXT,
    quantity_value_quantity DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    ) INCLUDE (quantity_value_quantity),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ) REFERENCES quantity_variable (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    ) REFERENCES execution (
        part_number,
        revision_number,
        process_name,
        process_version,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    )
);

CREATE TABLE waveform_value (
    waveform_value_length BIGINT NOT NULL GENERATED ALWAYS AS (cardinality(waveform_value_samples)) STORED,
    process_version TIMESTAMP WITH TIME ZONE,
    execution_start TIMESTAMP WITH TIME ZONE,
    waveform_value_start TIMESTAMP WITH TIME ZONE NOT NULL,
    part_number TEXT,
    revision_number TEXT,
    process_name TEXT,
    variable_path TEXT [],
    item_batch_number TEXT,
    item_serial_number TEXT,
    equipment_name TEXT,
    waveform_value_samples DOUBLE PRECISION [] NOT NULL,
    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ) REFERENCES waveform_variable (
        part_number,
        revision_number,
        process_name,
        process_version,
        variable_path
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    ) REFERENCES execution (
        part_number,
        revision_number,
        process_name,
        process_version,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    )
);

CREATE TABLE failure (
    process_version TIMESTAMP WITH TIME ZONE,
    execution_start TIMESTAMP WITH TIME ZONE,
    part_number TEXT,
    revision_number TEXT,
    item_batch_number TEXT,
    item_serial_number TEXT,
    process_name TEXT,
    equipment_name TEXT,
    failure_mode_name TEXT,

    PRIMARY KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        failure_mode_name,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    ) REFERENCES execution (
        part_number,
        revision_number,
        process_name,
        process_version,
        item_batch_number,
        item_serial_number,
        equipment_name,
        execution_start
    ),
    FOREIGN KEY (
        part_number,
        revision_number,
        process_name,
        process_version,
        failure_mode_name
    ) REFERENCES failure_mode (
        part_number,
        revision_number,
        process_name,
        process_version,
        failure_mode_name
    )
);
