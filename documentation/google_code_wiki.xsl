<?xml version='1.0'?>
<stylesheet xmlns="http://www.w3.org/1999/XSL/Transform" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:docbook="http://docbook.org/ns/docbook" version="1.0">
	<output method="text" indent="no"/>
	<strip-space elements="*"/>
	
	<variable name="imageBasePath">http://jessyink.googlecode.com/files/</variable>

	<template match="docbook:para">
		<value-of select="normalize-space(.)"/><text>
		

</text>
	</template>

	<template match="docbook:title">
		<value-of select="normalize-space(.)"/>
	</template>

	<template match="docbook:itemizedlist">
		<value-of select="normalize-space(.)"/>
	</template>

	<template match="docbook:listitem">
		<value-of select="normalize-space(.)"/>
	</template>

	<template match="docbook:programlisting">
		<value-of select="normalize-space(.)"/>
	</template>

	<template match="docbook:prompt">
		<value-of select="normalize-space(.)"/>
	</template>

	<template match="docbook:sect1/docbook:title">
		<text>= </text><apply-templates/><text> =
		
</text>
	</template>

	<template match="docbook:sect2/docbook:title">
		<text>== </text><apply-templates/><text> ==
		
</text>
	</template>

	<template match="docbook:sect3/docbook:title">
		<text>=== </text><apply-templates/><text> ===
		
</text>
	</template>

	<template match="docbook:itemizedlist">
		<apply-templates/><text>
</text>
	</template>

	<template match="docbook:listitem">
		<text>  * </text><value-of select="normalize-space(.)"/><text>
</text>
	</template>

	<template match="docbook:programlisting">
		<text>{{{
</text><apply-templates/>}}}<text>

</text>
	</template>

	<template match="docbook:prompt">
		<apply-templates/><text>
</text>
	</template>

	<template match="docbook:table">
		<apply-templates/><text>
</text>
	</template>

	<template match="docbook:table/docbook:title">
		<apply-templates/><text>
</text>
	</template>

	<template match="docbook:thead/docbook:row/docbook:entry">
		<text> *</text><apply-templates/><text>* ||</text>
	</template>

	<template match="docbook:row">
		<text>||</text><apply-templates/><text>
</text>
	</template>

	<template match="docbook:entry">
		<text> </text><apply-templates/><text> ||</text>
	</template>

	<template match="docbook:mediaobject">
		<text>
</text><apply-templates/><text>
</text>
	</template>
	
	<template match="docbook:imagedata">
		<text>[</text><xsl:copy-of select="$imageBasePath"/><value-of select="@fileref"/><text>]
</text>
	</template>

	<template match="docbook:caption">
		<text>
_</text><value-of select="normalize-space(.)"/><text>_
</text>
	</template>
</stylesheet>

