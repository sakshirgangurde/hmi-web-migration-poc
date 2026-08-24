async def create_nodes(server, idx):

    # ---------------------------------------------------------
    # Production Line
    # ---------------------------------------------------------

    production_line = await server.nodes.objects.add_object(
        idx,
        "ProductionLine1"
    )

    machine = await production_line.add_object(
        idx,
        "Machine1"
    )

    # ---------------------------------------------------------
    # Motor
    # ---------------------------------------------------------

    motor = await machine.add_object(
        idx,
        "Motor"
    )

    motor_speed = await motor.add_variable(
        idx,
        "MotorSpeed",
        1450.0
    )

    motor_current = await motor.add_variable(
        idx,
        "MotorCurrent",
        12.5
    )

    motor_power = await motor.add_variable(
        idx,
        "MotorPower",
        7.5
    )

    motor_temperature = await motor.add_variable(
        idx,
        "MotorTemperature",
        65.0
    )

    motor_running = await motor.add_variable(
        idx,
        "MotorRunning",
        True
    )

    motor_fault = await motor.add_variable(
        idx,
        "MotorFault",
        False
    )

    # ---------------------------------------------------------
    # Process
    # ---------------------------------------------------------

    process = await machine.add_object(
        idx,
        "Process"
    )

    process_temperature = await process.add_variable(
        idx,
        "ProcessTemperature",
        82.5
    )

    process_pressure = await process.add_variable(
        idx,
        "ProcessPressure",
        5.2
    )

    flow_rate = await process.add_variable(
        idx,
        "FlowRate",
        120.0
    )

    tank_level = await process.add_variable(
        idx,
        "TankLevel",
        72.0
    )

    vibration = await process.add_variable(
        idx,
        "Vibration",
        2.5
    )

    # ---------------------------------------------------------
    # Setpoints
    # ---------------------------------------------------------

    setpoints = await machine.add_object(
        idx,
        "Setpoints"
    )

    speed_setpoint = await setpoints.add_variable(
        idx,
        "SpeedSetpoint",
        1500.0
    )

    temperature_setpoint = await setpoints.add_variable(
        idx,
        "TemperatureSetpoint",
        85.0
    )

    pressure_setpoint = await setpoints.add_variable(
        idx,
        "PressureSetpoint",
        5.5
    )

    flow_rate_setpoint = await setpoints.add_variable(
        idx,
        "FlowRateSetpoint",
        125.0
    )

    # ---------------------------------------------------------
    # Commands
    # ---------------------------------------------------------

    commands = await machine.add_object(
        idx,
        "Commands"
    )

    start_command = await commands.add_variable(
        idx,
        "StartCommand",
        False
    )

    stop_command = await commands.add_variable(
        idx,
        "StopCommand",
        False
    )

    reset_command = await commands.add_variable(
        idx,
        "ResetCommand",
        False
    )

    # ---------------------------------------------------------
    # Mode
    # ---------------------------------------------------------

    mode = await machine.add_object(
        idx,
        "Mode"
    )

    auto_mode = await mode.add_variable(
        idx,
        "AutoMode",
        True
    )

    manual_mode = await mode.add_variable(
        idx,
        "ManualMode",
        False
    )

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    status = await machine.add_object(
        idx,
        "Status"
    )

    machine_running = await status.add_variable(
        idx,
        "MachineRunning",
        True
    )

    machine_ready = await status.add_variable(
        idx,
        "MachineReady",
        True
    )

    emergency_stop = await status.add_variable(
        idx,
        "EmergencyStop",
        False
    )

    fault_active = await status.add_variable(
        idx,
        "FaultActive",
        False
    )

    machine_status = await status.add_variable(
        idx,
        "MachineStatus",
        "RUNNING"
    )

    # ---------------------------------------------------------
    # Alarms
    # ---------------------------------------------------------

    alarms = await machine.add_object(
        idx,
        "Alarms"
    )

    high_temperature_alarm = await alarms.add_variable(
        idx,
        "HighTemperatureAlarm",
        False
    )

    high_pressure_alarm = await alarms.add_variable(
        idx,
        "HighPressureAlarm",
        False
    )

    motor_overload_alarm = await alarms.add_variable(
        idx,
        "MotorOverloadAlarm",
        False
    )

    low_level_alarm = await alarms.add_variable(
        idx,
        "LowLevelAlarm",
        False
    )

    high_vibration_alarm = await alarms.add_variable(
        idx,
        "HighVibrationAlarm",
        False
    )

    # ---------------------------------------------------------
    # Production
    # ---------------------------------------------------------

    production = await machine.add_object(
        idx,
        "Production"
    )

    production_count = await production.add_variable(
        idx,
        "ProductionCount",
        1250
    )

    reject_count = await production.add_variable(
        idx,
        "RejectCount",
        12
    )

    runtime_hours = await production.add_variable(
        idx,
        "RuntimeHours",
        342.5
    )

    batch_number = await production.add_variable(
        idx,
        "BatchNumber",
        "BATCH-2026-001"
    )

    # ---------------------------------------------------------
    # Writable Variables
    # ---------------------------------------------------------

    writable_variables = [
        speed_setpoint,
        temperature_setpoint,
        pressure_setpoint,
        flow_rate_setpoint,
        start_command,
        stop_command,
        reset_command,
        auto_mode,
        manual_mode,
    ]

    for variable in writable_variables:
        await variable.set_writable()

    # ---------------------------------------------------------
    # Return Node References
    # ---------------------------------------------------------

    return {
        # Motor
        "motor_speed": motor_speed,
        "motor_current": motor_current,
        "motor_power": motor_power,
        "motor_temperature": motor_temperature,
        "motor_running": motor_running,
        "motor_fault": motor_fault,

        # Process
        "process_temperature": process_temperature,
        "process_pressure": process_pressure,
        "flow_rate": flow_rate,
        "tank_level": tank_level,
        "vibration": vibration,

        # Setpoints
        "speed_setpoint": speed_setpoint,
        "temperature_setpoint": temperature_setpoint,
        "pressure_setpoint": pressure_setpoint,
        "flow_rate_setpoint": flow_rate_setpoint,

        # Commands
        "start_command": start_command,
        "stop_command": stop_command,
        "reset_command": reset_command,

        # Mode
        "auto_mode": auto_mode,
        "manual_mode": manual_mode,

        # Status
        "machine_running": machine_running,
        "machine_ready": machine_ready,
        "emergency_stop": emergency_stop,
        "fault_active": fault_active,
        "machine_status": machine_status,

        # Alarms
        "high_temperature_alarm": high_temperature_alarm,
        "high_pressure_alarm": high_pressure_alarm,
        "motor_overload_alarm": motor_overload_alarm,
        "low_level_alarm": low_level_alarm,
        "high_vibration_alarm": high_vibration_alarm,

        # Production
        "production_count": production_count,
        "reject_count": reject_count,
        "runtime_hours": runtime_hours,
        "batch_number": batch_number,
    }