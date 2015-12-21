SALUTATION = (
	(0, 'Mr'),
	(1, 'Mrs'),
	(2, 'Dr'),
	(3, 'Md'),
)
SUBSCRIPTION_STATUS = (
	(0, 'Not Subscribed'),
	(1, 'Subscribed'),
	(2, 'Expired'),
)
PROFILE_COMPLATION_STATUS = (
	(0, 'Supplier Information'),
	(1, 'Company Information'),
	(2, 'Company Revenue'),
	(3, 'Company Contact Info'),
	(4, 'License & Certificates'),
	(5, 'Product & Services'),
	(6, 'Certification'),
	(7, 'Completed'),
)
SERVICE_CODE_TYPE = (
	('naics', 'NAICS'),
	('sic', 'SIC'),
	('unspsc', 'UNSPSC'),
	('nigp', 'NIGP'),
	('cage', 'CAGE'),
)

SUBMISSION_STATUS = (
	(0, 'Profile Not Complate'),
	(1, 'Pending'),
	(2, 'Submitted'),
	(3, 'Error in Submission'),
)
ADDRESS_TYPE = (
	(0, 'Physical'),
	(1, 'Remitance'),
	(2, 'Mailing'),
	(3, 'Payment'),
)

CONTACT_TYPE = (
	(0, 'Primary'),
	(1, 'Secondary'),
	(2, 'Preparer'),
)

ANNUAL_SALE = (
	(0, "$0 - $499,000"),
	(1, "$500,000 - $1,000,000"),
	(2, "$1,000,001 - $5,000,000"),
)
ETHNICITIES = (
	(0, 'African American'),
	(1, 'Native American'),
	(2, 'Asia Pacific American'),
	(3, 'Subcontinent Asian American'),
	(4, 'Canadian Aboriginal'),
	(5, 'White (not Hisponic'),
	(6, 'Hisponic American'),
)

GEO_AREA = (
	(0, 'Local'),
	(1, 'Regional'),
	(2, 'National'),
	(3, 'International'),
)