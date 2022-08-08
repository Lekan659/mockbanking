""" This scripts contains constants of all the permissions that can 
    be assigned to a staff
"""

""" BASIC PERMISSIONS """
#
#This permission is required to register new customer
CAN_REGISTER_CUSTOMER = 'can_register_customer'
#
#This permission is required to view customer
CAN_VIEW_CUSTOMER = 'can_view_customer'
#
#This permission is required to initialize credit savings transaction
CAN_INITIALIZE_CREDIT_SAVINGS_TRANSACTION = "can_initialize_credit_savings_transaction"
#
#This permission is required to initialize debit savings transaction
CAN_INITIALIZE_DEBIT_SAVINGS_TRANSACTION = "can_initialize_debit_savings_transaction"

#This permission is required to view savings account
CAN_VIEW_SAVINGS_ACCOUNT = 'can_view_savings_account'

#This permission is required to view target savings account
CAN_VIEW_TARGET_SAVINGS_ACCOUNT = 'can_view_target_savings_account'

#This permission is required to view fixed deposit accounts
CAN_VIEW_FIXED_DEPOSIT_ACCOUNT = 'can_view_fixed_deposit_account'

""" MANAGEMENT PERMISSIONS """
#
#This permission is required to edit customer
CAN_EDIT_CUSTOMER = 'can_edit_customer'
#
#This permission is required to approve credit savings transaction
CAN_APPROVE_CREDIT_SAVINGS_TRANSACTION = "can_approve_credit_savings_transaction"
#
#This permission is required to decline credit pending savings transaction
CAN_DECLINE_CREDIT_SAVINGS_TRANSACTION = "can_decline_credit_savings_transaction"
#
#This permission is required to approve debit savings transaction
CAN_APPROVE_DEBIT_SAVINGS_TRANSACTION = "can_approve_debit_savings_transaction"
#
#This permission is required to decline debit pending savings transaction
CAN_DECLINE_DEBIT_SAVINGS_TRANSACTION = "can_decline_debit_savings_transaction"
#
#This permission is required to decline debit pending savings transaction
CAN_REVERSE_SAVINGS_TRANSACTION = "can_reverse_savings_transaction"
#
#This permission is required to add fixed deposit
CAN_ADD_FIXED_DEPOSIT = "can_add_fixed_deposit"

""" ADMINISTRATIVE PERMISSIONS """
#
#This permission is required to add new staff
CAN_ADD_STAFF = 'can_add_staff'
#
#This permission is required to view staff
CAN_VIEW_STAFF = 'can_view_staff'
#
#This permission is required to edit staff
CAN_EDIT_STAFF = 'can_edit_staff'
#
#This permission is required to edit staff permissions
CAN_EDIT_STAFF_PERMISSION = 'can_edit_staff_permission'

""" TELLER PERMISSIONS """
#
#This permission is required to add new staff
CAN_ADD_TILL = 'can_add_till'
#
#This permission is required to view staff
CAN_VIEW_TELLER = 'can_view_teller'
#
#This permission is required to edit staff
CAN_EDIT_TELLER = 'can_edit_teller'
#
#This permission is required to add new staff
CAN_EDIT_TILL = 'can_edit_till'
#
#This permission is required to add new staff
CAN_ADD_TELLER = 'can_add_teller'

